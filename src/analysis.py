import pandas as pd

def load_and_process_data():
    df = pd.read_csv("data/Nassau Candy Distributor.csv")

    # Date cleaning
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True, errors='coerce')

    df = df.dropna(subset=['Order Date', 'Ship Date'])

    # Lead Time
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df = df[df['Lead Time'] >= 0]

    # Factory Mapping
    factory_map = {
        "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
        "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
        "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
        "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
        "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
        "Laffy Taffy": "Sugar Shack",
        "SweeTARTS": "Sugar Shack",
        "Nerds": "Sugar Shack",
        "Fun Dip": "Sugar Shack",
        "Fizzy Lifting Drinks": "Sugar Shack",
        "Everlasting Gobstopper": "Secret Factory",
        "Hair Toffee": "The Other Factory",
        "Lickable Wallpaper": "Secret Factory",
        "Wonka Gum": "Secret Factory",
        "Kazookles": "The Other Factory"
    }

    df['Factory'] = df['Product Name'].map(factory_map)

    # Route
    df['Route'] = df['Factory'] + " → " + df['State/Province']

    return df


def get_route_analysis(df):
    route_df = df.groupby('Route').agg({
        'Lead Time': ['mean', 'count']
    }).reset_index()

    route_df.columns = ['Route', 'Avg Lead Time', 'Total Shipments']

    top_routes = route_df.sort_values(by='Avg Lead Time').head(10)
    worst_routes = route_df.sort_values(by='Avg Lead Time', ascending=False).head(10)

    return top_routes, worst_routes