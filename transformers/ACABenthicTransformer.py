from sqlalchemy import create_engine

class ACABenthicTransformer():
    def __init__(self):
        pass

    def transform(self):
        engine = create_engine('postgresql://{}@{}:{}/{}'.format("GOTECH", "127.0.0.1",5432, "coral_data"))
        table_exists_query = "SELECT to_regclass('staging.aca_benthic_4326');"
        transformation_query1 = """
        select 
            ogc_fid,
            class_name,
            area_sqkm,
            st_transform(wkb_geometry,4326) as wkb_geometry
        into
            staging.aca_benthic_4326
        from
            raw.aca_benthic ab;
        """
        
        transformation_query2="""
        select updategeometrysrid('staging','aca_benthic_4326','wkb_geometry',4326);
        """

        drop_table_query="""
        DROP TABLE staging.aca_benthic_4326;
        """

        with engine.connect() as con:
            rs = con.execute(table_exists_query)
            table_exists = rs.fetchone()[0]
            if table_exists:
                con.execute(drop_table_query)
            con.execute(transformation_query1)
            con.execute(transformation_query2)

        con.close()    