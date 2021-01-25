
# Format XML
``` 

import re
from xml.dom.minidom import parseString

cadena2 = '<?xml version="1.0" encoding="utf-8"?><Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02 pain.008.001.02.xsd"><CstmrDrctDbtInitn><GrpHdr><MsgId>2101250000010</MsgId><CreDtTm>2021-01-25T19:20:13</CreDtTm><NbOfTxs>1</NbOfTxs><CtrlSum>31.34</CtrlSum><InitgPty><Nm>EPIVENDING SISTEMAS S.L.</Nm><Id><OrgId><Othr><Id>ES06002B63585723</Id></Othr></OrgId></Id></InitgPty></GrpHdr><PmtInf><PmtInfId>PmtInfId-00001</PmtInfId><PmtMtd>DD</PmtMtd><BtchBookg>false</BtchBookg><NbOfTxs>1</NbOfTxs><CtrlSum>31.34</CtrlSum><PmtTpInf><SvcLvl><Cd>SEPA</Cd></SvcLvl><LclInstrm><Cd>CORE</Cd></LclInstrm><SeqTp>RCUR</SeqTp></PmtTpInf><ReqdColltnDt>2021-02-13</ReqdColltnDt><Cdtr><Nm>EPIVENDING SISTEMAS S.L.</Nm></Cdtr><CdtrAcct><Id><IBAN>ES5800751133410500025570</IBAN></Id></CdtrAcct><CdtrAgt><FinInstnId><BIC>BSABESBBXXX</BIC></FinInstnId></CdtrAgt><ChrgBr>SLEV</ChrgBr><CdtrSchmeId><Id><PrvtId><Othr><Id>ES06002B63585723</Id><SchmeNm><Prtry>SEPA</Prtry></SchmeNm></Othr></PrvtId></Id></CdtrSchmeId><DrctDbtTxInf><PmtId><InstrId>2101250000010</InstrId><EndToEndId>2101250000010</EndToEndId></PmtId><InstdAmt Ccy="EUR">31.34</InstdAmt><DrctDbtTx><MndtRltdInf><MndtId>21012500000000000003</MndtId><DtOfSgntr>2021-01-25</DtOfSgntr></MndtRltdInf></DrctDbtTx><DbtrAgt><FinInstnId><BIC>BSABESBBXXX</BIC></FinInstnId></DbtrAgt><Dbtr><Nm>EPIVENDING SISTEMAS S.L.</Nm></Dbtr><DbtrAcct><Id><IBAN>ES5800751133410500025570</IBAN></Id></DbtrAcct><RmtInf><Ustrd>INV/2020/12/0001</Ustrd></RmtInf></DrctDbtTxInf></PmtInf></CstmrDrctDbtInitn></Document>'

_xml_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)

def pretty_xml_old(xml_str, indent="  "):
    xml_re = _xml_re
    # avoid re-prettifying large amounts of xml that is fine
    if xml_str.count("\n") < 20:
        pxml = parseString(xml_str).toprettyxml(indent)
        return xml_re.sub('>\g<1></', pxml)
    else:
        return xml_str

print pretty_xml_old(cadena2)
``` 
