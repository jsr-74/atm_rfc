from flask import Flask, render_template,request, jsonify
from pyrfc import Connection
import json

# app = Flask(__name__)
app = Flask(__name__, static_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

global_atm_enc_data={}  #globaly access encrypted data  storing
@app.route("/Atm_encrypt_data", methods=["POST"])
def Atm_encrypt_data():
  
        
        dr = request.json            #recieving posting data 
        global_atm_enc_data['Ac_no'] = dr.get('ACC_NUM')
        global_atm_enc_data['Enc_Data'] = dr.get('ENCRIPT_DATA')
        return jsonify(  global_atm_enc_data )
   
    
  




@app.route("/Atmcard")
def Atmcard():
    ac_no =  global_atm_enc_data.get('Ac_no')
    cd =global_atm_enc_data.get('Enc_Data')
    #    Fill in your SAP system details
    conn = Connection(
    user="TRAINEE4",
    passwd="Lakshmi@74",
    ashost="192.168.1.49",  # or SAP router string
    sysnr="00",              # SAP system number (usually 00, 01...)
    client="100",            # SAP client number
    lang="EN"
    )



    
    result =  conn.call("ZJSR_ATM_DECRYPT_DATA",
                        IM_ENCRYPT_DATA = cd,
    IM_ACC_NO = str(ac_no) )

#     # print()     # "export parameters are stored in results as json format"
#    # Extract EX_JSON dictionary
    raw=result["EX_JSON"]              #"its not json format we must change to json"
    if isinstance(raw, str): 
        d = json.loads(raw)
    else:
        d = raw
    #Expiry date formatted
    exp_date = d["ExpDt"]  # e.g., "20301003"
    exp_formatted = str(exp_date[4:6]) + '/' +   str(exp_date[2:4])  # 10/30
    #ATM  number formatted ex 1111 2222 3333 4444
    Atm_no = " ".join(d["AtmNo"][i:i+4] for i in range(0, len(d["AtmNo"]), 4))
    Atm_digit = d["AtmDgt"]
    h_name = d["Hname"]
    Atm_cvv = d["AtmCvv"]
    Atm_ref = d["AtmRef"]
    
    

    Final_data= {"Hname": h_name ,"AtmNo": Atm_no,"AtmDgt": Atm_digit,"ExpDt": exp_formatted,"AtmCvv": Atm_cvv,"AtmRef": Atm_ref }  
    return render_template("index.html",data=Final_data)#, card_no=c_no,data=d, exp=exp_formatted)
   
if __name__ == "__main__":
    # app.run(debug=True) "only in laptop"
     app.run(host="0.0.0.0", port=5000,debug=True) #other device also"
    
