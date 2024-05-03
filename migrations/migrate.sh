#alembic downgrade -1
REVISION=$(alembic current | awk '{print $7}')
REV=$(echo $REVISION | sed "s/'//g")
if [ -z "$REVISION" ]
then
   echo "migrate starting"
else
  alembic revision --rev-id "$REV"
fi
alembic downgrade -1
alembic upgrade head
alembic revision --autogenerate -m "$(date +%F)"
alembic -x data=true upgrade head || alembic upgrade head

# #!/bin/bash

# # SQLAlchemy ve Alembic migrate işlemleri

# # Alembic upgrade komutu ile tüm revizyonları yürüt
# alembic upgrade head

# # Revizyon otomatik oluşturulması
# alembic revision --autogenerate -m "$(date +%F)"

# # Migrate işlemi
# alembic -x data=true upgrade head || alembic upgrade head
