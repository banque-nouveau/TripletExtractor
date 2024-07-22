from openai import OpenAI
from datetime import datetime
from models import TripletResponse
from pathlib import Path
import instructor
from dotenv import load_dotenv
import pandas as pd
import boto3
from botocore.exceptions import ClientError


__all__ = ['KGTriplets']


class KGTriplets():
    def __init__(self, use_minio=False, miniobucket='mybucket'):
        load_dotenv()
        self.client = instructor.from_openai(OpenAI())
        self.use_minio = use_minio
        self.miniobucket = miniobucket
        self.s3_client = None

        if self.use_minio:
            s3 = boto3.client('s3',
                  endpoint_url='http://localhost:9000',
                  aws_access_key_id='minio_access_key',
                  aws_secret_access_key='minio_secret_key')
            # Create a bucket

            try:
                bucket_existence = s3.head_bucket(Bucket=miniobucket)
                if bucket_existence["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    print("Bucket exists\n")  
            except ClientError as e:
                    print(e)
                    print("Bucket does not exist, creating new bucket\n")
                    s3.create_bucket(Bucket=miniobucket)
            self.s3_client = s3
        
    
    def get_knowledge_graph_representation(self,
                                           text_chunk:str,
                                           static_prompt_fname:str='prompts/blackrock_prompt.txt',
                                           model:str="gpt-4o" ):
        """
        returns the knowledge graph triplets from a text chunk using openAI models.

        Parameters
        ----------

        Returns
        -------

        Example
        -------
        If the text chunk is "Apple Inc. is set to introduce the new iPhone 14 in the technology sector this month." The expected output is:
        response.input = "Apple Inc. is set to introduce the new iPhone 14 in the technology sector this month."
        response.subject = ['Apple Inc.', 'Apple Inc.']
        response.subject_type = ['COMP', 'COMP']
        response.relation = ['Introduce', 'Operate_In']
        response.object = ['iPhone 14', 'Technology Sector']
        response.object_type = ['PRODUCT', 'SECTOR']
        """

        with open(static_prompt_fname, 'r') as file:
            static_prompt = file.read()
        prompt =  static_prompt + text_chunk
        response = self.client.chat.completions.create(model=model,
                                                temperature=0.0, 
                                                top_p=0.3,
                                                response_model=TripletResponse,
                                                messages= [{ "role": "user", "content": prompt }])
    
        return response

    @staticmethod
    def wrap(response):

        unique_id = datetime.now().strftime('%Y-%m-%d-%H:%M:%S:%f')    
        sze = len(response.subject) 
        cols = ['subject', 'subject_type', 'relation', 'object', 'object_type']
        mydict = {}
        mydict['subject'] = response.subject
        mydict['subject_type'] = response.subject_type
        mydict['relation'] = response.relation
        mydict['object'] = response.object
        mydict['object_type'] = response.object_type
        idx = list(unique_id for i in range(sze))
        output_df = pd.DataFrame(mydict, index=idx)

        input_df = pd.DataFrame({'input': response.input}, index=[unique_id])

        return input_df, output_df

    def serialize_kg(self, news_prompt, output_path,
                     static_prompt_fname='prompts/blackrock_prompt.txt',  
                     model='gpt-4o',
                     ):

        """
        returns a list of list of entities and relations along with entity types

        Parameters
        ----------

        Returns
        -------

        Example
        -------
        If the news prompt is "Apple Inc. is set to introduce the new iPhone 14 in the technology sector this month." and the output path is "output.parquet", the expected output is:
        A parquet file named "output.parquet" will be created with the content "Apple Inc. is set to introduce the new iPhone 14 in the technology sector this month."
        """
        
        response = self.get_knowledge_graph_representation(news_prompt, static_prompt_fname, model)
        input_df, output_df = KGTriplets.wrap(response)
        unique_id = input_df.index.values[0]
        input_fname = f'output_{unique_id}.parquet'
        output_fname = f'input_{unique_id}.parquet'
        output_path = Path(output_path)
        input_df.to_parquet(output_path/input_fname)
        output_df.to_parquet(output_path/output_fname)


        if self.use_minio:
            s3 = self.s3_client
            s3.upload_file(output_path/input_fname, self.miniobucket, input_fname)
            s3.upload_file(output_path/output_fname, self.miniobucket, output_fname)
            # List objects in the bucket
            response = s3.list_objects(Bucket=self.miniobucket)
            for obj in response.get('Contents', []):
                print(obj['Key'])
        return None