from controller.base import BaseController
from core.security import get_password_hash, verify_password

from sqlalchemy.orm import Session

from typing import Any, Dict, Optional, Union

import models
import schemas


class PatronController(BaseController[models.Patron, schemas.PatronCreate, schemas.PatronUpdate, schemas.PatrondDelete]):

    def __init__(self, model):
        super().__init__(model)
    
    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[models.Patron]:
        return db.query(models.Patron).filter(models.Patron.email == email).first()
    
    def update(
            self, db: Session, *, db_obj: models.Patron, obj_in: Union[schemas.PatronUpdate, Dict[str, Any]]
    ) -> models.Patron:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        if update_data['password']:
            hashed_password = get_password_hash(update_data['password'])
            del update_data["password"]
            update_data['hashed_password'] = hashed_password
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[models.Patron]:
        auth_user = self.get_by_email(db, email=email)
        if not auth_user:
            print('if1')
            return None
        if not verify_password(password, auth_user.password):
            print('if2')
            return None
        
        return auth_user
    
    def is_active(self, user: models.Patron) -> bool:
        return user.is_active


patron = PatronController(models.Patron)