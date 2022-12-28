#-*- coding: utf-8 -*-

from odoo import fields, models, api, _
import base64
import tempfile
import ftplib
from odoo.exceptions import UserError


class FtpUpload(models.TransientModel):
    _name = "ftp.upload"
    _description = "Ftp Upload"

    file = fields.Binary('File')
    file_name = fields.Char('File Name')

    def action_upload_ftp(self):
        file = base64.b64decode(self.file)
        file_name = self.file_name
        path = tempfile.gettempdir() + '/' + file_name
        params = self.env['ir.config_parameter'].sudo()
        try:
            ftp = ftplib.FTP()
            host = params.get_param('ftp.host')
            port = int(params.get_param('ftp.port'))
            user = params.get_param('ftp.user')
            password = params.get_param('ftp.password')
            folder_path = '/one/'
            ftp.connect(host, port)
            try:
                ftp.login(user, password)
            except:
                raise UserError(_("Failed Ftp Login"))
            try:
                file = open(path, "rb")
            except:
                raise UserError(_("Failed Txt Open"))
            try:
                ftp.storbinary(f"STOR {folder_path}/{file_name}", file)
            except Exception as error:
                print(error)
                raise UserError(_(error))
            file.close()
            ftp.close()

        except Exception as error:
            raise UserError(error)

