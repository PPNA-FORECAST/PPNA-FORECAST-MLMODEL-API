ppna_points_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "location": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "string"},
                    "longitude": {"type": "string"},
                    "sample": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "date": {"type": "string", "format": "date"},
                                "temp": {"type": "string"},
                                "ppt": {"type": "string"},
                                "ppna": {"type": "string"}
                            },
                            "required": ["date", "temp", "ppt", "ppna"]
                        }
                    }
                },
                "required": ["latitude", "longitude", "sample"]
            }
        },
        "required": ["location"]
    }
}