"""
Hometown Map Generator
This script creates an interactive map of hometown locations using Folium and Mapbox.
It geocodes addresses, adds custom markers, and creates interactive popups with images.
"""

import folium
import pandas as pd
import requests
import time

# ============================================================================
# CONFIGURATION - Replace with your own values
# ============================================================================

# Your Mapbox Access Token
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiZ3JhaGFtZ29iYmVsIiwiYSI6ImNtbHRtdHJoODAxdjQzZm9pbzk5YzEzY3QifQ.wJeHCKx6rQG4W2tdhi60mA'

# Your Mapbox Style (Format: username/style_id)
# Example: 'mapbox/streets-v12' or 'your_username/your_style_id'
MAPBOX_STYLE = 'grahamgobbel/cmm0t56o8000001ql1i440xul'

# CSV file with your locations
CSV_FILE = 'hometown_locations.csv'

# Output HTML file
OUTPUT_FILE = 'hometown_map.html'

# Map center (will be calculated from your locations)
# Or set manually: [latitude, longitude]
MAP_CENTER = None

# Initial zoom level
ZOOM_START = 12

# ============================================================================
# ICON COLORS FOR DIFFERENT LOCATION TYPES
# ============================================================================
ICON_COLORS = {
    'restaurant': 'red',
    'park': 'green',
    'cultural': 'blue',
    'landmark': 'purple',
    'school': 'orange',
    'exercise': 'lightgreen',
    'store': 'pink',
    'activity': 'cadetblue',
    'default': 'gray'
}

# Icon symbols for different types
ICON_SYMBOLS = {
    'restaurant': 'cutlery',
    'park': 'tree',
    'cultural': 'university',
    'landmark': 'star',
    'school': 'education',
    'exercise': 'heart',
    'store': 'shopping-cart',
    'activity': 'flag',
    'default': 'info-sign'
}


# ============================================================================
# GEOCODING FUNCTION
# ============================================================================
def geocode_address(address, access_token):
    """
    Geocode an address using Mapbox Geocoding API.
    
    Args:
        address (str): The address to geocode
        access_token (str): Your Mapbox access token
    
    Returns:
        tuple: (latitude, longitude) or (None, None) if geocoding fails
    """
    # Mapbox Geocoding API v6 endpoint
    geocode_url = f'https://api.mapbox.com/search/geocode/v6/forward?q={address}&access_token={access_token}'
    
    try:
        response = requests.get(geocode_url)
        response.raise_for_status()
        data = response.json()
        
        # Extract coordinates from the first result
        if data.get('features') and len(data['features']) > 0:
            coordinates = data['features'][0]['geometry']['coordinates']
            # Mapbox returns [longitude, latitude], we need [latitude, longitude]
            longitude, latitude = coordinates
            print(f"✓ Geocoded: {address} -> ({latitude:.6f}, {longitude:.6f})")
            return latitude, longitude
        else:
            print(f"✗ No results found for: {address}")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error geocoding {address}: {e}")
        return None, None


# ============================================================================
# MAIN FUNCTION
# ============================================================================
def create_hometown_map():
    """
    Main function to create the hometown map.
    Reads CSV, geocodes addresses, creates map with markers.
    """
    print("=" * 60)
    print("HOMETOWN MAP GENERATOR")
    print("=" * 60)
    
    # Step 1: Read CSV file
    print(f"\n📂 Reading locations from {CSV_FILE}...")
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"✓ Found {len(df)} locations")
    except FileNotFoundError:
        print(f"✗ Error: Could not find {CSV_FILE}")
        print("Please create a CSV file with columns: name, address, type, description, image_url")
        return
    
    # Step 2: Geocode all addresses
    print("\n🌍 Geocoding addresses...")
    latitudes = []
    longitudes = []
    
    for idx, row in df.iterrows():
        lat, lon = geocode_address(row['Address'], MAPBOX_ACCESS_TOKEN)
        latitudes.append(lat)
        longitudes.append(lon)
        # Be nice to the API - add a small delay between requests
        time.sleep(0.5)
    
    df['latitude'] = latitudes
    df['longitude'] = longitudes
    
    # Remove rows where geocoding failed
    df_valid = df.dropna(subset=['latitude', 'longitude'])
    print(f"\n✓ Successfully geocoded {len(df_valid)} out of {len(df)} locations")
    
    if len(df_valid) == 0:
        print("✗ No valid locations to map. Exiting.")
        return
    
    # Step 3: Calculate map center
    if MAP_CENTER is None:
        center_lat = df_valid['latitude'].mean()
        center_lon = df_valid['longitude'].mean()
    else:
        center_lat, center_lon = MAP_CENTER
    
    print(f"\n🗺️  Map center: ({center_lat:.6f}, {center_lon:.6f})")
    
    # Step 4: Create Folium map with Mapbox tiles
    print("\n🎨 Creating map with Mapbox style...")
    
    # Mapbox tile URL format
    tiles_url = f'https://api.mapbox.com/styles/v1/{MAPBOX_STYLE}/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={MAPBOX_ACCESS_TOKEN}'
    
    # Create the map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=ZOOM_START,
        tiles=tiles_url,
        attr='Mapbox'
    )
    
    # Step 5: Add markers for each location
    print("\n📍 Adding markers to map...")
    for idx, row in df_valid.iterrows():
        # Get icon color and symbol based on location type
        location_type = row['Type'].lower() if pd.notna(row['Type']) else 'default'
        icon_color = ICON_COLORS.get(location_type, ICON_COLORS['default'])
        icon_symbol = ICON_SYMBOLS.get(location_type, ICON_SYMBOLS['default'])
        
        # Create popup HTML with image and information
        popup_html = f"""
        <div style="width: 300px; font-family: Arial, sans-serif;">
            <h3 style="margin: 0 0 10px 0; color: #333;">{row['Name']}</h3>
            <img src="{row['Image_URL']}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 5px; margin-bottom: 10px;">
            <p style="margin: 5px 0; color: #666; font-style: italic;">
                <strong>Type:</strong> {row['Type'].title()}
            </p>
            <p style="margin: 10px 0; color: #333; line-height: 1.5;">
                {row['Description']}
            </p>
        </div>
        """
        
        # Create custom icon
        icon = folium.Icon(
            color=icon_color,
            icon=icon_symbol,
            prefix='glyphicon'
        )
        
        # Add marker to map
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['Name'],  # Shows on hover
            icon=icon
        ).add_to(m)
        
        print(f"  ✓ Added marker: {row['Name']} ({location_type})")
    
    # Step 6: Save map to HTML file
    print(f"\n💾 Saving map to {OUTPUT_FILE}...")
    m.save(OUTPUT_FILE)
    print(f"✓ Map saved successfully!")
    
    print("\n" + "=" * 60)
    print("🎉 COMPLETE! Open the HTML file in your browser to view the map.")
    print("=" * 60)


# ============================================================================
# RUN THE SCRIPT
# ============================================================================
if __name__ == "__main__":
    create_hometown_map()