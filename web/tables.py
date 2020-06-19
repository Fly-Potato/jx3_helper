# 所有的表结构
import sqlalchemy as sa


metadata = sa.MetaData()
tbl = sa.Table('tbl', metadata
               , sa.Column('id', sa.Integer, primary_key=True)
               , sa.Column('val', sa.String(255)))

user = sa.Table('user', metadata,
                sa.Column('id', sa.BigInteger, primary_key=True),  # QQ
                sa.Column('password', sa.String(255)))


def get_tables():
    return [tbl]
