# Try
```  
# -*- coding: utf-8 -*-
import xmlrpc.client
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


def get_remote_uid(self):
        try:
            common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % self.desc)
            uid = common.authenticate(self.remote_db, self.user, self.password, {})
        except OSError:
            raise ValidationError(_('Debe indicar el protocolo (http://, https://).'))
        except ConnectionRefusedError:
            raise ValidationError(_('No se pudo conectar con el servidor, verifique la URL y vuelva a intentar.'))
        except xmlrpc.client.Fault:
            raise ValidationError(_('No se pudo conectar con el servidor, verifique el nombre de la base de datos.'))
        except xmlrpc.client.ProtocolError:
            raise ValidationError(_('El protocolo indicado no es correcto (http://, https://)'))
        except AttributeError:
            raise ValidationError(_('Algo está mal configurado, verifique antes de continuar.'))
        if not uid:
            raise ValidationError(_('Usuario o clave inválida.'))
        return uid
```  



```  
if insertalo:
  try:
    product_id = models.execute_kw(db,uid,password,'res.partner','create',[vals])
  except:
    print("Error ========================================================================= ")
```  



```
def _validate_facturae(self, xml_string):
        facturae_schema = etree.XMLSchema(etree.parse(self._get_facturae_schema_file()))
        try:

            facturae_schema.assertValid(etree.fromstring(xml_string))
        except Exception as e:
            logger.warning("The XML file is invalid against the XML Schema Definition")
            logger.warning(xml_string)
            logger.warning(e)
            raise UserError(
                _(
                    "The generated XML file is not valid against the official "
                    "XML Schema Definition. The generated XML file and the "
                    "full error have been written in the server logs. Here "
                    "is the error, which may give you an idea on the cause "
                    "of the problem : %s"
                )
                % str(e)
            )
        return True

```
