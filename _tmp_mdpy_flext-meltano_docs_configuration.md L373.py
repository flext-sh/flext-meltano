# from flext-meltano/docs/configuration.md:373
# Write Singer catalog
catalog_data = {
    "streams": [{"tap_stream_id": "users", "schema": {...}, "metadata": [...]}]
}

write_result = file_manager.write_singer_catalog(catalog_data, "output/catalog.json")```
### Configuration Backup

