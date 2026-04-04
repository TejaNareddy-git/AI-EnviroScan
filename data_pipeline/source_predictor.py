def predict_source(row):
    pm25 = row.get("pm25", 0)
    no2 = row.get("no2", 0)
    so2 = row.get("so2", 0)
    o3 = row.get("o3", 0)
    co = row.get("co", 0)

    # 🚗 Vehicular Pollution
    if no2 > 50 and co > 200:
        return "Vehicular"

    # 🏭 Industrial Pollution
    elif so2 and so2 > 20:
        return "Industrial"

    # 🔥 Burning (waste / biomass)
    elif pm25 > 100 and co > 300:
        return "Burning"

    # 🌾 Agricultural
    elif pm25 > 80 and o3 < 50:
        return "Agricultural"

    # 🌿 Natural
    else:
        return "Natural"