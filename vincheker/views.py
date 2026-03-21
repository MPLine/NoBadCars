from django.shortcuts import render
import requests

def calculate_risk(make, model, year):
    """
    Simple risk logic:
    - Si gen Make oswa Model ki manke → High
    - Si ane < 2000 → Medium
    - Sinon → Low
    """
    if not make or not model:
        return "High"
    try:
        year_int = int(year)
    except:
        return "Medium"
    if year_int < 2000:
        return "Medium"
    return "Low"

def home(request):
    data = None
    if request.method == "POST":
        vin = request.POST.get('vin')
        # NHTSA API
        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json'
    
        try:
            response = requests.get(url).json()
        
            results = response.get('Results', [])
            for r in results:
                print(r)
                print("-------")
            # Extract main info
            make = next((r['Value'] for r in results if r['Variable'] == 'Make'), '')
            model = next((r['Value'] for r in results if r['Variable'] == 'Model'), '')
            year = next((r['Value'] for r in results if r['Variable'] == 'Model Year'), '')
            Trim = next((r['Value'] for r in results if r['Variable'] == 'Trim'), '')
            doors = next((r['Value'] for r in results if r['Variable'] == 'Doors'), '')
            company = next((r['Value'] for r in results if r['Variable'] == 'Plant Company Name'), '')
            body = next((r['Value'] for r in results if r['Variable'] == 'Body Class'), '')
            
            
            risk = calculate_risk(make, model, year)
            data = {
                'vin': vin,
                'make': make,
                'model': model,
                'year': year,
                'company':company,
                'doors':doors,
                'trim':Trim,
                'body':body,
                'risk':risk,
            }
        except:
            print('error')
    return render(request, 'vincheker/home.html', {'data': data})