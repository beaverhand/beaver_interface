from backend.data_methods import DataLoader
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_community.llms import VLLM
import yaml
import os
import sys
with open("../config.yaml", "r") as file:
    config = yaml.safe_load(file)

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

def generate_summaries(all_pdf_file_loc, write_to_pickle = 1):
    llm = VLLM(
        model=config['llm_model']['model'],
        trust_remote_code=config['llm_model']['trust_remote_code'],
        max_new_tokens=config['llm_model']['max_new_tokens'],
        max_model_len=config['llm_model']['max_model_len'],
        top_p=config['llm_model']['top_p'],
        temperature=config['llm_model']['temperature'],
        vllm_kwargs={"quantization": config['llm_model']['quantization']}
    )
    resume_summary_list = []
    resume_text_list = []
    for pdf_file_loc in all_pdf_file_loc:
        resume_text = DataLoader.extract_text_from_pdf(pdf_file_loc)
        resume_text_list.append(resume_text)
        template = config['template']
        prompt = PromptTemplate.from_template(template)
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        resume_summary_list.append(llm_chain.invoke(resume_text)['text'])
    return [(u_id,resume_text,summary) for  u_id,resume_text,summary in 
            zip([int(x.split('.')[0].split('/')[-1]) for x in all_pdf_file_loc],
                resume_text_list,
                resume_summary_list)]