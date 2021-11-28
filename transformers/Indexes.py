from sqlalchemy import create_engine

class Indexes():
    def __init__(self):
        pass

    def add_spatial_index(self,index_name,schema,table,field,conn):
        query=f'CREATE INDEX {index_name} ON {schema}.{table} USING GIST ({field});'
        conn.execute(query)

        
    def create_indexes(self):
        engine = create_engine('postgresql://{}@{}:{}/{}'.format("GOTECH", "127.0.0.1",5432, "coral_data"))
        with engine.connect() as conn:
            self.add_spatial_index('calipso_geom_idx',
                                    'raw',
                                    'calipso',
                                    'geometry',
                                    conn)
            self.add_spatial_index('aca_benthic_4326_geom_idx',
                                    'staging',
                                    'aca_benthic_4326',
                                    'wkb_geometry',
                                    conn)