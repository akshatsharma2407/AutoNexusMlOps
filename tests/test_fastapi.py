import unittest
from fastapi.testclient import TestClient
from FastApi_app.main import app

class FastAPITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
    
    def test_endpoints(cls):
        response = cls.client.post("/prediction", json={
                                            "Unnamed: 0": 0,
                                            "Model_Year": 1990,
                                            "Mileage": 2463,
                                            "Brand_Name": "Audi",
                                            "Model_Name": "Model Y",
                                            "Stock_Type": "New",
                                            "Exterior_Color": "gray",
                                            "Interior_Color": "gray",
                                            "Drivetrain": "AWD",
                                            "Km/L": 0,
                                            "Fuel_Type": "Electric",
                                            "Accidents_Or_Damage": True,
                                            "Clean_Title": True,
                                            "One_Owner_Vehicle": True,
                                            "Personal_Use_Only": True,
                                            "Level2_Charging": 0,
                                            "Dc_Fast_Charging": 0,
                                            "Battery_Capacity": 70,
                                            "Expected_Range": 300,
                                            "Gear_Spec": 5,
                                            "Engine_Size": 2.4,
                                            "Cylinder_Config": "V8",
                                            "Valves": 0,
                                            "Km/L_e_City": 31,
                                            "Km/L_e_Hwy": 50,
                                            "City": "string",
                                            "STATE": "Alaska"
                                            })
        cls.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()