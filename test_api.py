import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5001"

def test_create_user():
    """Test creating a new user"""
    print("=== Testing CREATE User ===")
    url = f"{BASE_URL}/api/users"
    data = {"phone_number": "0123456789"}
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result.get('user', {}).get('id')
        else:
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_get_users():
    """Test getting all users"""
    print("\n=== Testing GET All Users ===")
    url = f"{BASE_URL}/api/users"
    
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_get_user(user_id):
    """Test getting a specific user"""
    print(f"\n=== Testing GET User {user_id} ===")
    url = f"{BASE_URL}/api/users/{user_id}"
    
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_update_user(user_id):
    """Test updating a user"""
    print(f"\n=== Testing UPDATE User {user_id} ===")
    url = f"{BASE_URL}/api/users/{user_id}"
    data = {"phone_number": "0987654321"}
    
    response = requests.put(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_delete_user(user_id):
    """Test deleting a user"""
    print(f"\n=== Testing DELETE User {user_id} ===")
    url = f"{BASE_URL}/api/users/{user_id}"
    
    response = requests.delete(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def main():
    print("Starting API Tests...")
    
    # Test sequence
    user_id = test_create_user()
    test_get_users()
    
    if user_id:
        test_get_user(user_id)
        test_update_user(user_id)
        test_get_user(user_id)  # Check after update
        test_delete_user(user_id)
        test_get_users()  # Check after deletion
    
    print("\nAPI Tests completed!")

if __name__ == "__main__":
    main()
