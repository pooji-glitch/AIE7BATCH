"""
Fix for the LangSmith dataset creation HTTPError in the notebook.

Replace the problematic cell with this code:
"""

# Replace this cell in your notebook:
"""
from langsmith import Client
import uuid

client = Client()

dataset_name = "Loan Synthetic Data"

# Try to create the dataset, but handle the case where it already exists
try:
    langsmith_dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Loan Synthetic Data"
    )
    print(f"✅ Successfully created new dataset: '{dataset_name}'")
except Exception as e:
    if "already exists" in str(e):
        print(f"⚠️  Dataset '{dataset_name}' already exists. Attempting to use existing dataset...")
        # Try to get the existing dataset
        try:
            datasets = client.list_datasets()
            existing_dataset = next((ds for ds in datasets if ds.name == dataset_name), None)
            
            if existing_dataset:
                langsmith_dataset = existing_dataset
                print(f"✅ Found existing dataset: '{dataset_name}' (ID: {existing_dataset.id})")
            else:
                # If we can't find it, create with a unique name
                unique_name = f"{dataset_name}_{uuid.uuid4().hex[:8]}"
                print(f"🔄 Creating new dataset with unique name: '{unique_name}'")
                langsmith_dataset = client.create_dataset(
                    dataset_name=unique_name,
                    description="Loan Synthetic Data"
                )
        except Exception as inner_e:
            print(f"❌ Error accessing existing datasets: {inner_e}")
            # Create with a unique name as fallback
            unique_name = f"{dataset_name}_{uuid.uuid4().hex[:8]}"
            print(f"🔄 Creating fallback dataset: '{unique_name}'")
            langsmith_dataset = client.create_dataset(
                dataset_name=unique_name,
                description="Loan Synthetic Data"
            )
    else:
        print(f"❌ Unexpected error: {e}")
        raise e
"""

# Alternative simpler approach - just use a unique name:
"""
from langsmith import Client
import uuid

client = Client()

# Use a unique name to avoid conflicts
dataset_name = f"Loan Synthetic Data_{uuid.uuid4().hex[:8]}"

langsmith_dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="Loan Synthetic Data"
)

print(f"✅ Created dataset: '{dataset_name}'")
""" 