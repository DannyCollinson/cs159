import os
from openai import OpenAI
import requests

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def get_molecular_data(molecule_id):
    # Example function to get data from ChEMBL
    response = requests.get(f'https://www.ebi.ac.uk/chembl/api/data/molecule/{molecule_id}')
    return response
def get_protein_data(protein_id):
    """
    Retrieve protein data from UniProt database using their API.
    
    Args:
    protein_id (str): The UniProt ID of the protein.
    
    Returns:
    dict: A dictionary containing the protein data.
    """
    url = f"https://www.ebi.ac.uk/proteins/api/proteins/{protein_id}"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve data for protein ID {protein_id}: {response.status_code}")
def create_prompt(molecule_data, protein_data):
    prompt = f"""
    Given the following molecular data:
    {molecule_data}
    
    And the following protein data:
    {protein_data}
    
    Please predict the interaction and provide reasoning for your prediction.
    """
    return prompt
def generate_prediction(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content   
def main():
    molecule_id = 'CHEMBL6329'  # Example molecule ID
    protein_id = 'P12345'     # Example protein ID

    molecule_data = get_molecular_data(molecule_id)
    protein_data = get_protein_data(protein_id)  # Implement this function similarly

    prompt = create_prompt(molecule_data, protein_data)
    prediction = generate_prediction(prompt)

    print("Prediction and reasoning:", prediction)

if __name__ == "__main__":
    main()
