#!/usr/bin/env python3
"""
Fix for the LangSmith dataset creation HTTPError.
This script shows how to handle the case where a dataset with the same name already exists.
"""

from langsmith import Client
import uuid

def create_dataset_safely(dataset_name="Loan Synthetic Data", description="Loan Synthetic Data"):
    """
    Safely create a LangSmith dataset, handling the case where it already exists.
    
    Args:
        dataset_name (str): The name of the dataset to create
        description (str): The description of the dataset
    
    Returns:
        The created or existing dataset
    """
    client = Client()
    
    try:
        # Try to create the dataset
        langsmith_dataset = client.create_dataset(
            dataset_name=dataset_name,
            description=description
        )
        print(f"✅ Successfully created new dataset: '{dataset_name}'")
        return langsmith_dataset
        
    except Exception as e:
        if "already exists" in str(e):
            print(f"⚠️  Dataset '{dataset_name}' already exists. Attempting to use existing dataset...")
            
            # Try to get the existing dataset
            try:
                datasets = client.list_datasets()
                existing_dataset = next((ds for ds in datasets if ds.name == dataset_name), None)
                
                if existing_dataset:
                    print(f"✅ Found existing dataset: '{dataset_name}' (ID: {existing_dataset.id})")
                    return existing_dataset
                else:
                    # If we can't find it, create with a unique name
                    unique_name = f"{dataset_name}_{uuid.uuid4().hex[:8]}"
                    print(f"🔄 Creating new dataset with unique name: '{unique_name}'")
                    
                    langsmith_dataset = client.create_dataset(
                        dataset_name=unique_name,
                        description=description
                    )
                    print(f"✅ Successfully created dataset: '{unique_name}'")
                    return langsmith_dataset
                    
            except Exception as inner_e:
                print(f"❌ Error accessing existing datasets: {inner_e}")
                # Create with a unique name as fallback
                unique_name = f"{dataset_name}_{uuid.uuid4().hex[:8]}"
                print(f"🔄 Creating fallback dataset: '{unique_name}'")
                
                langsmith_dataset = client.create_dataset(
                    dataset_name=unique_name,
                    description=description
                )
                print(f"✅ Successfully created fallback dataset: '{unique_name}'")
                return langsmith_dataset
        else:
            print(f"❌ Unexpected error: {e}")
            raise e

if __name__ == "__main__":
    # Example usage
    dataset = create_dataset_safely()
    print(f"Dataset ID: {dataset.id}")
    print(f"Dataset Name: {dataset.name}") 