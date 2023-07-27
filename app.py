import code
import os 
import sqlite3
from urllib import request
from flask import Flask
import requests
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as pyp
from datetime import datetime, timedelta
from urllib import request
from flask import Flask,render_template,request,make_response,redirect
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


#　グローバル変数の宣言
search_history=[]

app=Flask(__name__,static_folder='./static')


@app.route("/", methods=['GET'])
def index():
    User_name = request.cookies.get('char_name')
    if User_name is None:
        return redirect('/page')

    

    result_price = []
    result_line = []

    favorite_list = []
    favorite_unique_list = []
    item_list=[]




    tag_item = request.cookies.get('tag_wepon')


    if tag_item is not None:
        favorite = tag_item.split(",")
    else:
        favorite=["39649","39630"] 

    for data in favorite:
        favorite_list += recipe_id_search(data)
    favorite_unique_list = list(set(favorite_list))
    f_rireki = get_buy(favorite_unique_list,False)

    for data in f_rireki:
            cookie_value = request.cookies.get(data[4])  # data[4]をクッキー名として指定
            if data[0] == 0 and cookie_value is not None:
                cookie_parts = cookie_value.split(',')
                data[0] = int(cookie_parts[0])
                data[1] = cookie_parts[1]
                data[2] = int(cookie_parts[2])
    

    for data2 in favorite:
        price = result_print_favorite(data2, f_rireki)
        item_name = item_matching_id(data2)
        sell_price = get_sell(data2)
        sell_price2 = sell_price[2]
        profit = round(((sell_price2 - price) / price) * 100, 1)
        result_line = [data2, item_name, price, sell_price2, profit]
        result_price.append(result_line)
        result_line = []
        profit = 0

    for data4 in f_rireki:
        item_id=data4[4]
        item_name=item_matching_id(data4[4])
        IL = result_IL(data4[4])
        UVS_link=universalis_link(data4[4])
        icon=result_image(item_name)
        item_line=(item_id,item_name,IL,icon,UVS_link)
                
        if data4[1]!='' and item_recipe_check(data4[4])==True:
            item_list.append(item_line)
        elif data4[1]!='' and item_recipe_check(data4[4])==False:
            item_list.append(item_line)
        # elif data4[1]=="" and item_recipe_check(data4[4])==True:
        #     item_list.append(item_line)
        elif data4[1]=='' and item_recipe_check(data4[4])==False:
            item_list.append(item_line)
        


        



    item_list.sort(reverse=True, key=lambda x: x[2])


    print_data = ""
    for data3 in result_price:
        img = result_image(data3[1])
        print_data += "<li class='favorite_list'><input type='checkbox' name='item_tag' class='favorite_item 'value='" + data3[0] + "'><button class='item_button_favorite' name='wepon' value=" + data3[0] + "><h3>" + img +data3[1]+ "</h3><p>原価 : " +str(data3[2]) + " Gill<br>販売価格平均 : "+str(data3[3])+" Gill<br>利益率:"+str(data3[4])+"%<p></button></li>"

    print_data = "<form method='GET' action='category'><h2>お気に入りリスト</h2><ul class='favorite_category'>" + print_data + "</ul></form>"

    print_data2=""
    for print_list in item_list:
        print_data2 +=  """<li class='F_item_list2'>
                                <div class="item_list_image">"""+print_list[4] +print_list[3]+"""</div>
                                <button class='item_button2' name='history' value=""" + str(print_list[0]) + """>
                                    <h3>""" +print_list[1]+ """</h3>
                                    <p>IL:"""+str(print_list[2])+"""<p>
                                </button>
                            </li>"""
        
    print_data=print_data+"<div id='favorite_material'><form method='GET' action='/history'><h2>お気に入りリストで用いた材料履歴</h2><ul class='item_list'>" + print_data2 +"</ul></form></div>"

    return render_template('top.html', title="Milvaneth", message1='<div id="top_main">'+print_data+'</div>')

    


@app.route("/page",methods=['GET'])
def page():
    select = request.args.get('page')
    if select=='0':
        return index()
        

    else:
        char_name = request.cookies.get('char_name')
        buyer_DC = request.cookies.get('buyer_DC')
        buyer_WD = request.cookies.get('buyer_WD')
        seller_DC = request.cookies.get('seller_DC')
        seller_WD = request.cookies.get('seller_WD')

        return render_template('config.html', title="Milvaneth", char_name=char_name, buyer_DC=buyer_DC, buyer_WD=buyer_WD, seller_DC=seller_DC, seller_WD=seller_WD)



@app.route("/config", methods=['POST'])
def config():
    if request.method == 'POST':
        char_name = request.form.get("name")
        buyer_DC = request.form.get("buyer_Datacenter_select")
        buyer_WD = request.form.get("buyer_World_select")
        seller_DC = request.form.get("seller_Datacenter_select")
        seller_WD = request.form.get("seller_World_select")

        # レスポンスオブジェクトを作成
        resp = make_response(redirect('/page'))

        # クッキーを削除
        resp = delete_cookie(resp, "char_name")
        resp = delete_cookie(resp, "buyer_DC")
        resp = delete_cookie(resp, "buyer_WD")
        resp = delete_cookie(resp, "seller_DC")
        resp = delete_cookie(resp, "seller_WD")

        # 新しい値をクッキーに保存
        resp.set_cookie("char_name", char_name, max_age=2419200)
        resp.set_cookie("buyer_DC", buyer_DC, max_age=2419200)
        resp.set_cookie("buyer_WD", buyer_WD, max_age=2419200)
        resp.set_cookie("seller_DC", seller_DC, max_age=2419200)
        resp.set_cookie("seller_WD", seller_WD, max_age=2419200)

        return resp
   
    return redirect('/page')


def delete_cookie(response, name):
    response.delete_cookie(name)
    return response


@app.route("/category", methods=['GET'])
def category():
    wepon2 = []
    item_list = []
    item_tag_result_list = []
    select = 0
    DB_name = ["One-handed_sword", "Two-handed_axe", "Two-handed_sword", "Gunblade", "Two-handed_spear", "Two-handed_sickle", "Melee_weapon", "samurai_Sword", "duble_Sword", "Bow",
               "Throwing_Weapon", "Two-Handed_Curse", "Magic_Book", "Rapier", "One-Handed_Illusion","Two-handed_Illusion", "Magic_Tome_(Scholar_Only)", "Arms", "Sage" ,
               "Woodworking_tools (main_tools)", "Woodworking_tools_(secondary_tools)", "Blacksmithing_tools_(main_tools)", "Blacksmithing_tools_(secondary_tools)", "Armor_tools_(main_tools)",
               "armor_tools_(secondary_tools)", "metal_carving_tools_(main_tools)", "metal_carving_tools_(secondary_tools)", "leather_working_tools_(main_tools)", "leather_working_tools_(secondary_tools)",
               "Sewing_tools_(main_tool)","Sewing_tools_(secondary_tool)", "Alchemy_tools_(main_tool)", "Alchemy_tools_(secondary_tool)", "Cooking_tools (main_tool)", "Cooking_tools_(secondary_tool)",
               "mining_tools_(main_tools)", "mining_tools_(secondary_tools)", "gardening_tools_(main_tools)", "gardening_tools_(secondary_tools)", "fishing_tools_(main_tools)", "fishing_bait", "shield","head_armor","body_armor","hand_armor","leg_armor","foot_armor",
               "Medicine", "Foodstuff", "Cooking", "Seafood", "Stone", "Metal", "Wood", "Cloth", "Leather", "Aggregate", "Alchemy", "dyes","components","catalysts",
               "Miscellaneous_Goods", "Miscellaneous_Goods_(Seasonal)", "Minions", "Orchestrion_Sheet_Music","Earrings","Necklaces","Bracelets","Rings","materia"]
    item_category_grooup={14:"14,15",19:"19,20",21:"21,22",23:"23,24",25:"25,26",27:"27,28",29:"29,30",31:"31,32",33:"33,34",35:"35,26",37:"37,38"}
    select = request.args.get('wepon')
    
    if select is not None and int(select) >= 0 and int(select) < 99:
        if select in item_category_grooup:
            select = item_category_grooup[select]
        wepon = select
        wepon2 = wepon[0:2]

        item_list = item_DB_matching(DB_name[int(wepon2)])
        item_list.sort(reverse=True, key=lambda x: x[4])

        print_data = ""
        for data in item_list:
            img = result_image(data[2])
            print_data += "<li class='item_list'><input type='checkbox' name='item_tag' id='item_list_" + str(data[0]) + "' value='" + str(data[0]) + "'><button class='item_button' name='wepon' value=" + str(data[0]) + "><h3>" + img + data[2] + "</h3><p> IL : " + str(data[4]) + "<p></button></li>"

        print_data = "<div id='main'><ul class='item_category'>" + print_data + "</ul><div>"

        resp = make_response(render_template('index2.html', title="Milvaneth", config="main_contents", message1=print_data))

        return resp


    elif select is not None and int(select) > 100:

        crystal_list=[]
        old_record=datetime.now()

        flag=False
        crystal=["2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19"]
        for data in crystal:
            cookie_value = request.cookies.get(data)
            if cookie_value is not None:
                    cookie_parts = cookie_value.split(',')
                    if cookie_parts[0] != '0':
                         if old_record > datetime.fromtimestamp(int(cookie_parts[3])):
                            old_record = datetime.fromtimestamp(int(cookie_parts[3]))
                            flag=True
        nowtime=datetime.now()
        days_elapsed=(nowtime-old_record).days
        
        if days_elapsed>30 or flag==False:
            crystal_list=get_buy(crystal,True)


        item_id = select
        list1 = recipe_id_search(item_id)
        if list1== []:
            list1=[item_id] 
        else:
            pass
        switchstate = request.cookies.get('switchState')
        if switchstate=="on":
            list2 = get_buy(list1,False)
            list2=list2+crystal_list
            resp = make_response()
            resp=cookie_write(list2,item_id,True)
        else:
            list2 = get_buy_all(list1)
            list2=list2+crystal_list
            resp = make_response()
            resp=cookie_write(list2,item_id,False)
        return resp
    else:
        return redirect('/')




def cookie_write(list2,item_id,cookie_flag):

    if cookie_flag=="on":
        for data in list2:
            cookie_value = request.cookies.get(data[4])  # data[4]をクッキー名として指定
            if cookie_value is not None:
                cookie_parts = cookie_value.split(',')
                if cookie_parts[0] != '0' and data[0] == 0:
                    data[0] = int(cookie_parts[0])
                    data[1] = cookie_parts[1]
                    data[2] = int(cookie_parts[2])
                    data[3] = float(cookie_parts[3]) if len(cookie_parts) >= 4 else 0.0
    else:pass

          
    flag=item_recipe_check(item_id)
    if flag==True:
        print_data = result_print(item_id, list2)
    else:
        return history()

    resp = make_response(render_template('result.html', title="Milvaneth", message1='<div id="result">'+ print_data +'</div>'))

    if cookie_flag=="on":
        for data in list2:
            if data[1] != "":   
                li_tag = data[1].split("\012")
                # カットする場合はここでカットして終了
                i = 0
                print_cookie = ""
                for data2 in li_tag:
                    print_cookie += data2
                    i += 1
                    if i == 6:
                        break
                
                # 5行目までの処理を行う
                # 例: 表示する
                print_cookie = print_cookie + "</div></div></ul>"
                data[1] = print_cookie

                cookie_value = str(data[0]) + "," + print_cookie + "," + str(data[2])+","+str(data[5])+","+str(data[6])
                resp.set_cookie(data[4], value=cookie_value, max_age=2419200)
                i=0
    return resp




@app.route("/history",methods=['GET'])
def history():

    icon=""

    item_id=0
    item_id = request.args.get("history")
    switchstate = request.cookies.get('switchState')
    global search_history
    print_data=""
  
    if switchstate=="on":
        search_history=get_buy([item_id],True)
    else:
        search_history=get_buy_all([item_id])

    index=0
    for sublist in search_history:
        if item_id in sublist:
            index = search_history.index(sublist)
            break

    average_nq=search_history[index][0]
    print_data_new=search_history[index][1]
    average_hq=search_history[index][2]
    print_data_old=search_history[index][3]
    item_id=search_history[index][4]

    if average_nq==0:
        average_nq_text="取引情報がありません"
    else:
        average_nq_text=str(average_nq)+" ギル"
    if average_hq==0:
        average_hq_text="取引情報がありません"
    else:
        average_hq_text=str(average_hq)+" ギル"

    if print_data=="":
        print_data="取引情報はありません"
    
    item_line_Big= result_tool_link_Big(item_matching_id(item_id)) 
    icon=result_image_L(item_matching_id(item_id))
    description_text=result_description(item_id)

    description='''<div class='history_material'>
                        <div id=history_icon>'''+icon+'''
                            <h2>'''+item_line_Big+'''</h2>
                            <h3>'''+description_text+'''</h3>
                            <h4>NQの平均価格: '''+average_nq_text+''' </h4>
                            <h4>HQの平均価格: '''+average_hq_text+''' </h4>
                        </div>
                        <div id=result_history>'''


    print_data2= description+"<h2>購入履歴</h2><ul>"+print_data_new+"</ul>"

    return render_template('history.html',title="Milvaneth",message1='<div id="main">'+print_data2+'</div></div>') 
    






def process_tag_cookie(print_data, item_tag, item_list):
    # 既存のクッキーからtag_weponとitem_id_oldを取得
    tag_wepon_cookie = request.cookies.get('tag_wepon')
    item_id_old_cookie = request.cookies.get('item_id_old')

    # tag_weponが存在する場合、カンマ区切りの文字列をリストに変換
    if tag_wepon_cookie:
        tag_wepon_list = tag_wepon_cookie.split(',')
    else:
        tag_wepon_list = []

    # item_id_oldが存在する場合、カンマ区切りの文字列をリストに変換
    if item_id_old_cookie:
        item_id_old_list = item_id_old_cookie.split(',')
    else:
        item_id_old_list = []

    # item_id_oldに登録されているidをtag_weponから除外
    new_tag_wepon_list = [item_id for item_id in tag_wepon_list if item_id not in item_id_old_list]

    # item_tagで受け取ったidをtag_weponに追加
    new_tag_wepon_list.extend(item_tag)

    # クッキーを更新
    tag_wepon_str = ','.join(new_tag_wepon_list)
    item_id_str = ','.join(str(item[0]) for item in item_list)

    resp = make_response(render_template('index2.html', title="Milvaneth", config="main_contents", message1=print_data))
    resp.set_cookie('tag_wepon', tag_wepon_str)
    resp.set_cookie('item_id_old', item_id_str)

    return resp





@app.route("/materia",methods=['GET'])
def materia():

    select = request.args.get('materia')
    address="https://xivapi.com"

    item_list = item_DB_matching("materia")
    item_list.sort(reverse=True, key=lambda x: x[4])

    print_data = ""
    for data in item_list:
        img = "<img class='icon' src=\""+address+data[3]+"\">"
        print_data += "<li class='item_list'><input type='checkbox' name='item_tag' id='item_list_" + str(data[0]) + "' value='" + str(data[0]) + "'><button class='item_button' name='history' value=" + str(data[0]) + "><h3>" + img + data[2] + "</h3><p> IL : " + str(data[4]) + "<p></button></li>"

    print_data = "<div id='main'><ul class='item_category'>" + print_data + "</ul><div>"

    resp = make_response(render_template('materia.html', title="Milvaneth", config="main_contents", message1=print_data))

    return resp




@app.route("/fc_craft",methods=['GET'])
def fc_craft():
    item_list=[]

    select = request.args.get('category')
    item_list=fc_craft_matching(select)

    print_data = ""
    address="https://xivapi.com"

    for data in item_list:
        img = "<img class='icon' src=\""+address+str(data[3])+"\">"
        print_data += "<li class='item_list'><input type='checkbox' name='item_tag' id='item_list_" + str(data[0]) + "' value='" + str(data[0]) + "'><button class='item_button' name='item' value=" + str(data[0]) + "><h3>" + img + data[1] + "</h3><p> カテゴリ : " + str(data[2]) + "<p></button></li>"

    print_data = "<div id='main'>><ul class='item_category'>" + print_data + "</ul><div>"

    resp = make_response(render_template('fc_craft.html', title="Milvaneth", config="main_contents", message1=print_data))

    return resp


@app.route("/craft",methods=['GET'])

def fc_craft_result():
    print_data=""
    search_item_list=[]
    getbuy_search_list=[]

    select = request.args.get('item')
    item_list=fc_craft_id_matching(select)
    switchstate = request.cookies.get('switchState')

    sequence=sequence_read(item_list)
    sub_sequence=[]

    for data in sequence:
        for data2 in data:
            item_id = data2[0]
            id=frame_check(item_id)
            if id=="":
                search_item_list.append(item_id)
            else:
                item_list=fc_craft_id_matching(id)
                sub_sequence=sequence_read(item_list)
                for data3 in sub_sequence:
                    for data4 in data3:
                        search_item_list.append(data4[0])


    for data in search_item_list:
        getbuy_search_list += [data]+recipe_id_search(data)
    
    getbuy_unique_list = list(set(getbuy_search_list))

    if switchstate=="on":
        rireki = get_buy(getbuy_unique_list,True)
    else:
        rireki = get_buy_all(getbuy_unique_list)

    for data in rireki:
        cookie_value = request.cookies.get(data[4])  # data[4]をクッキー名として指定
        if data[0] == 0 and cookie_value is not None:
            cookie_parts = cookie_value.split(',')
            data[0] = int(cookie_parts[0])
            data[1] = cookie_parts[1]
            data[2] = int(cookie_parts[2])

    print_data=result_company_print(select,sequence,sub_sequence,rireki)



    resp = make_response(render_template('fc_craft.html', title="Milvaneth", config="main_contents", message1=print_data))

    return resp


def sequence_read(item_list):

    select_sequence=[]
    sequence_line=[]
    sequence=[]



    for i in range(5,12,1):
        if item_list[i]!="":
            select_sequence.append(item_list[i])
    
    sequence_list=fc_craft_sequence_matching(select_sequence)

    for data in sequence_list:
        for i in range(1,33,3):
            if data[i]!='':
                sequence_line.append([data[i],data[i+1],data[i+2]])
        sequence.append(sequence_line)
        sequence_line=[]

    return sequence



def frame_check(id):

    return_id=""
    frame=[[26508,21792],
        [26509,21793],
        [26510,21794],
        [26511,21795],
        [26512,21796],
        [26513,21797],
        [26514,21798],
        [26515,21799],
        [26516,22526],
        [26517,22527],
        [26518,22528],
        [26519,22529],
        [26520,23903],
        [26521,23904],
        [26522,23905],
        [26523,23906],
        [26524,24344],
        [26525,24345],
        [26526,24346],
        [26527,24347]]
    
    for data in frame:
        if id==str(data[0]):
            return_id=data[1]
            break

    return return_id



def result_print_favorite(main_id, result_list):

    item_name = item_matching_id(main_id)
    print(item_name)
    first_recipe = item_recipe(main_id)
    result_amount = int(item_recipe2(main_id))
    all_sum = 0
    sub_sum1 = 0
    sub_sum2 = 0
    sub_sum3 = 0
    for data in first_recipe:
        sub_sum1=0
        item_id = data[0]
        item_name = item_matching_id(data[0])
        amount = int(data[1])
        result_data_page = search_list(result_list, item_id)
        result_data = result_list[result_data_page]
        result_average_nq = result_data[0]
        nq_sum = result_average_nq * amount
        sub_sum1+=nq_sum
        result_amount2 = int(item_recipe2(item_id))
        second_recipe = item_recipe(item_id)

        if item_recipe_check(data[0]) == True:
            sub_sum2=0
            for data2 in second_recipe:
                item_id2 = str(data2[0])
                amount2 = int(data2[1])
                item_name2 = item_matching_id(item_id2)
                print(item_name2)
                result_data_page2 = search_list(result_list, item_id2)
                result_data2 = result_list[result_data_page2]
                result_average_nq2 = result_data2[0]
                nq_sum2 = result_average_nq2 * amount2
                print(nq_sum2)
                sub_sum2 += nq_sum2
                third_recipe = item_recipe(item_id2)
                result_amount3 = int(item_recipe2(item_id2))
                if item_recipe_check(data2[0]) == True:
                    sub_sum3 = 0
                    for data3 in third_recipe:
                        item_id3 = str(data3[0])
                        amount3 = int(data3[1])
                        item_name3 = item_matching_id(data3[0])
                        print(item_name3)
                        result_data_page3 = search_list(result_list, item_id3)
                        result_data3 = result_list[result_data_page3]
                        result_average_nq3 = result_data3[0]
                        sub_sum3 += result_average_nq3 * amount3
                        print(sub_sum3)
                    result_item_price3 = round(sub_sum3 / result_amount3)
                    if result_average_nq2 == 0:
                        all_sum += result_item_price3 * amount2
                    elif result_item_price3 == 0:
                        all_sum += result_average_nq2 * amount2
                    else:
                        all_sum += min(result_average_nq2, result_item_price3) * amount2
                else:
                    pass
            result_item_price2 = round(sub_sum2 / result_amount2)
            if result_average_nq == 0:
                all_sum += result_item_price2 * amount
            elif result_item_price2 == 0:
                all_sum += result_average_nq * amount
            else:
                all_sum += min(result_average_nq, result_item_price2) * amount
        else:
            all_sum+=sub_sum1

    print(item_name)
    print(all_sum)
 
    result_price = round(all_sum / result_amount)

    # 初期化
    all_sum = 0
    sub_sum1 = 0
    sub_sum2 = 0
    sub_sum3 = 0

    return result_price
 





def flame_culcurate(main_id,first_recipe,result_list):

    all_sum=0

    first_floor_sum=0
    second_floor_sum=0
    third_floor_sum=0



    for data in first_recipe:
        first_floor_sum=0
        for data2 in data:

            first_floor_nq=0
            first_floor_hq=0

            first_floor_item_id=data2[0]
            first_floor_quantity=int(data2[1])
            first_floor_set=data2[2]
            
            first_floor_item=itemname_DB_matching(first_floor_item_id)
            first_floor_item_name=first_floor_item[2]

            result_data_page=search_list(result_list,first_floor_item_id)
            first_floor_item_data=result_list[result_data_page]
            first_floor_nq=first_floor_item_data[0]
            first_floor_price_nq=first_floor_nq*first_floor_quantity*first_floor_set
            first_floor_hq=first_floor_item_data[2]
            first_floor_price_hq=first_floor_hq*first_floor_quantity*first_floor_set

            first_floor_sum += first_floor_price_nq
           
            if item_recipe_check(first_floor_item_id)==True:
                second_recipe=item_recipe(first_floor_item_id)

                for data3 in second_recipe:
                    
                    
                    second_floor_nq=0
                    second_floor_hq=0

                    second_floor_item_id=data3[0]
                    second_floor_quantity=int(data3[1])

                    second_floor_item=itemname_DB_matching(second_floor_item_id)
                    second_floor_item_name=second_floor_item[2]

                    result_data_page=search_list(result_list,second_floor_item_id)
                    second_floor_item_data=result_list[result_data_page]
                    second_floor_nq=second_floor_item_data[0]
                    second_floor_price_nq=second_floor_nq*int(second_floor_quantity)
                    second_floor_hq=second_floor_item_data[2]
                    second_floor_price_hq=second_floor_hq*int(second_floor_quantity)
                    result_amount2 = int(item_recipe2(second_floor_item_id)) 
                    second_floor_sum += second_floor_price_nq
                    
                    if item_recipe_check(second_floor_item_id)==True:
                        third_recipe=item_recipe(second_floor_item_id)

                        for data3 in third_recipe:

                            third_floor_nq=0
                            third_floor_hq=0

                            third_floor_item_id=data3[0]
                            third_floor_quantity=int(data3[1])

                            third_floor_item=itemname_DB_matching(third_floor_item_id)
                            third_floor_item_name=third_floor_item[2]

                            result_data_page=search_list(result_list,third_floor_item_id)
                            third_floor_item_data=result_list[result_data_page]
                            third_floor_nq=third_floor_item_data[0]
                            third_floor_price_nq=third_floor_nq*int(third_floor_quantity)
                            third_floor_hq=third_floor_item_data[2]
                            third_floor_price_hq=third_floor_hq*int(third_floor_quantity)

                            third_floor_sum += third_floor_price_nq
                            result_amount3 = int(item_recipe2(third_floor_item_id)) 

                        second_floor_sum_re=(second_floor_sum-(second_floor_nq*second_floor_quantity)+third_floor_sum)*second_floor_quantity
                        if second_floor_sum>second_floor_sum_re:
                            second_floor_sum=second_floor_sum_re

                        third_floor_sum=0
                    else:
                        pass

                result_item_price2 = round(second_floor_sum / result_amount2)

                if first_floor_nq == 0:
                    all_sum += result_item_price2 * first_floor_quantity*first_floor_set
                elif result_item_price2 == 0:
                    all_sum += second_floor_price_nq
                else:
                    all_sum += min(first_floor_nq , result_item_price2) * first_floor_quantity*first_floor_set
            
                second_floor_sum=0

            else:

                all_sum+=first_floor_price_nq
                first_floor_sum=0

    result_amount=int(item_recipe2(main_id))
    all_sum = round(all_sum / result_amount)


    return all_sum






def result_company_print(main_id,first_recipe,sub_sequence,result_list):

    print_data=""
    all_sum=0
    search_item=get_sell(main_id)                               #完成品の販売履歴を読み込み
    search_item_average_hq=search_item[2]                       #HQの取引履歴を変数に格納
    search_item_avelage_nq=search_item[0]                       #NQの取引履歴を変数に格納

    first_floor_sum=0
    second_floor_sum=0
    third_floor_sum=0

    print_data_second_floor=""
    print_data_third_floor=""

    for data in first_recipe:
        first_floor_sum=0
        for data2 in data:
            

            first_floor_nq=0
            first_floor_hq=0

            print_data_first_floor_nq=""
            print_data_first_floor_hq=""

            first_floor_item_id=data2[0]
            first_floor_quantity=int(data2[1])
            first_floor_set=data2[2]
            frame_id=frame_check(first_floor_item_id)
            if frame_id!="":
                frame_price=flame_culcurate(frame_id,sub_sequence,result_list)
                first_floor_nq=frame_price
                first_floor_hq=0
            else:

                result_data_page=search_list(result_list,first_floor_item_id)
                first_floor_item_data=result_list[result_data_page]
                first_floor_nq=first_floor_item_data[0]
                
                first_floor_hq=first_floor_item_data[2]


            first_floor_item=itemname_DB_matching(first_floor_item_id)
            first_floor_item_name=first_floor_item[2]
            first_floor_price_nq=first_floor_nq*first_floor_quantity*first_floor_set
            first_floor_price_hq=first_floor_hq*first_floor_quantity*first_floor_set

            first_floor_sum += first_floor_price_nq

            UVS_URL=universalis_link(first_floor_item_id)
            icon=result_image(first_floor_item_name)                            #1段目の材料アイコンを呼び出し↓へ出力
            market_icon=result_history_icon(first_floor_item_name)
            item_line1=result_tool_link(first_floor_item_name)
            


            if first_floor_hq==0:
                print_data_first_floor_hq="<h3>"+item_line1+"<img src='./static/HQicon.png' class='HQ'>の取引は確認できませんでした。</h3>"
            else:
                print_data_first_floor_hq="<h3>"+item_line1+"<img src='./static/HQicon.png' class='HQ'>"+str(first_floor_hq)+" ギル x"+str(first_floor_quantity*first_floor_set)+" 個 = "+str(first_floor_price_hq)+" ギル</h3>"   
            if first_floor_nq==0:
                print_data_first_floor_nq="<h3>"+item_line1+"の取引は確認できませんでした。</h3>"
            else:
                print_data_first_floor_nq="<h3>"+item_line1+" "+str(first_floor_nq)+" ギル x"+str(first_floor_quantity*first_floor_set)+" 個 = "+str(first_floor_price_nq)+" ギル</h3>"

            first_floor_item_text="""<div class=material>
                                        <div class='icon_T'>"""+UVS_URL+icon+market_icon+"""</div>
                                        """+print_data_first_floor_hq + print_data_first_floor_nq+"""
                                    </div>"""
            print_data+=first_floor_item_text
            
            if item_recipe_check(first_floor_item_id)==True:
                second_recipe=item_recipe(first_floor_item_id)

                print_data_second_floor=""

                for data3 in second_recipe:
                    
                    
                    second_floor_nq=0
                    second_floor_hq=0

                    print_data_second_floor_nq=""
                    print_data_second_floor_hq=""

                    second_floor_item_id=data3[0]
                    second_floor_quantity=int(data3[1])

                    second_floor_item=itemname_DB_matching(second_floor_item_id)
                    second_floor_item_name=second_floor_item[2]

                    result_data_page=search_list(result_list,second_floor_item_id)
                    second_floor_item_data=result_list[result_data_page]
                    second_floor_nq=second_floor_item_data[0]
                    second_floor_price_nq=second_floor_nq*int(second_floor_quantity)
                    second_floor_hq=second_floor_item_data[2]
                    second_floor_price_hq=second_floor_hq*int(second_floor_quantity)

                    second_floor_sum += second_floor_price_nq

                    UVS_URL=universalis_link(second_floor_item_id)
                    icon=result_image(second_floor_item_name)
                    market_icon=result_history_icon(second_floor_item_name)
                    item_line2=result_tool_link(second_floor_item_name)
                    result_amount2 = int(item_recipe2(second_floor_item_id))

                    if second_floor_hq==0:
                        print_data_second_floor_hq="<h3>"+item_line2+"<img src='./static/HQicon.png' class='HQ'>の取引は確認できませんでした。</h3>"
                    else:
                        print_data_second_floor_hq="<h3>"+item_line2+"<img src='./static/HQicon.png' class='HQ'>"+str(second_floor_hq)+" ギル x"+str(second_floor_quantity)+" 個 = "+str(second_floor_price_hq)+" ギル</h3>"   
                    if second_floor_nq==0:
                        print_data_second_floor_nq="<h3>"+item_line2+"の取引は確認できませんでした。</h3>"
                    else:
                        print_data_second_floor_nq="<h3>"+item_line2+" "+str(second_floor_nq)+" ギル x"+str(second_floor_quantity)+" 個 = "+str(second_floor_price_nq)+" ギル</h3>"

                    second_floor_item_text="""<div class=sub_material>
                                                <div class='icon_T'>"""+UVS_URL+icon+market_icon+"""</div>
                                                """+print_data_second_floor_hq + print_data_second_floor_nq+"""

                                            </div>"""
                    
                    print_data_second_floor+=second_floor_item_text
                    
                    if item_recipe_check(second_floor_item_id)==True:
                        third_recipe=item_recipe(second_floor_item_id)

                    
                        print_data_third_floor=""

                        for data3 in third_recipe:

                            third_floor_nq=0
                            third_floor_hq=0

                            print_data_third_floor_nq=""
                            print_data_third_floor_hq=""

                            third_floor_item_id=data3[0]
                            third_floor_quantity=int(data3[1])

                            third_floor_item=itemname_DB_matching(third_floor_item_id)
                            third_floor_item_name=third_floor_item[2]

                            result_data_page=search_list(result_list,third_floor_item_id)
                            third_floor_item_data=result_list[result_data_page]
                            third_floor_nq=third_floor_item_data[0]
                            third_floor_price_nq=third_floor_nq*int(third_floor_quantity)
                            third_floor_hq=third_floor_item_data[2]
                            third_floor_price_hq=third_floor_hq*int(third_floor_quantity)

                            third_floor_sum += third_floor_price_nq

                            UVS_URL=universalis_link(third_floor_item_id)
                            icon=result_image(third_floor_item_name)
                            market_icon=result_history_icon(third_floor_item_name)
                            item_line3=result_tool_link(third_floor_item_name)
                            result_amount3 = int(item_recipe2(third_floor_item_id)) 

                            if third_floor_hq==0:
                                print_data_third_floor_hq="<h3>"+item_line3+"<img src='./static/HQicon.png' class='HQ'>の取引は確認できませんでした。</h3>"
                            else:
                                print_data_third_floor_hq="<h3>"+item_line3+"<img src='./static/HQicon.png' class='HQ'>"+str(third_floor_hq)+" ギル x"+str(third_floor_quantity)+" 個 = "+str(third_floor_price_hq)+" ギル</h3>"   
                            if third_floor_nq==0:
                                print_data_third_floor_nq="<h3>"+item_line3+"の取引は確認できませんでした。</h3>"
                            else:
                                print_data_third_floor_nq="<h3>"+item_line3+" "+str(third_floor_nq)+" ギル x"+str(third_floor_quantity)+" 個 = "+str(third_floor_price_nq)+" ギル</h3>"

                            third_floor_item_text="""<div class=sub_material>
                                                        <div class='icon_T'>"""+UVS_URL+icon+market_icon+"""</div>
                                                        """+print_data_third_floor_hq + print_data_third_floor_nq+"""
                                                    </div>"""
                            
                            print_data_third_floor+=third_floor_item_text
                        

                        # result_item_price3 = round(third_floor_sum / result_amount3)

                        # if second_floor_nq == 0:
                        #     all_sum += third_floor_sum * second_floor_quantity
                        # elif result_item_price3 == 0:
                        #     all_sum += second_floor_price_nq
                        # else:
                        #     all_sum += min(second_floor_nq, result_item_price3) * second_floor_quantity

                        second_floor_sum_re=(second_floor_sum-(second_floor_nq*second_floor_quantity)+third_floor_sum)*second_floor_quantity
                        if second_floor_sum>second_floor_sum_re:
                            second_floor_sum=second_floor_sum_re



                                                
                        second_floor_item_text="""<div class='material_etc'>
                                                    <h3>"""+item_line2+"""を原料から作成した場合""" +str(third_floor_sum)+"""ギル x""" +str(second_floor_quantity)+""" 個 = """+str(third_floor_sum*second_floor_quantity)+""" ギル　▼</h3>
                                                </div>"""
                        #print_data+="<details><summary>"+second_floor_item_text+"</summary>"+print_data_third_floor+"</details>"

                        print_data_second_floor=print_data_second_floor + "<details><summary>"+second_floor_item_text+"</summary>"+print_data_third_floor+"</details>"
                        third_floor_sum=0
                    else:

                        pass



                result_item_price2 = round(second_floor_sum / result_amount2)

                if first_floor_nq == 0:
                    all_sum += result_item_price2 * first_floor_quantity*first_floor_set
                elif result_item_price2 == 0:
                    all_sum += second_floor_price_nq
                else:
                    all_sum += min(first_floor_nq , result_item_price2) * first_floor_quantity*first_floor_set
            

                first_floor_item_text="""<div class='material_etc'>
                                            <h3>"""+item_line1+"""を原料から作成した場合""" +str(second_floor_sum)+"""ギル x""" +str(first_floor_quantity*first_floor_set)+""" 個 = """+str(second_floor_sum*first_floor_quantity*first_floor_set)+""" ギル　▼</h3>
                                        </div>"""
                print_data+="<details><summary>"+first_floor_item_text+"</summary>"+print_data_second_floor+"</details>"
                second_floor_sum=0

            else:

                all_sum+=first_floor_sum
                first_floor_sum=0

    result_amount=int(item_recipe2(main_id))
    all_sum = round(all_sum / result_amount)




    item_line1= result_tool_link(item_matching_id(main_id))           #検索された完成品idからボタンを作成
    item_line_Big= result_tool_link_Big(item_matching_id(main_id))    #検索された完成品idからロードストーンURLを作成
    icon=result_image_L(item_matching_id(main_id))                    #検索された完成品idから大型アイコンURLを作製
    UVS_URL=universalis_link_Big(main_id)
    player_info=read_charactor()

    if search_item_average_hq != 0:                                      #完成品のHQの取引履歴が存在した場合
        print_data="""<div id='result'>"""+player_info+"""
                                    <div class=icons>"""+UVS_URL+icon+"""</div>
                                    <div class=result_item>
                                        <h2>"""+item_line_Big+"""<img src='./static/HQicon.png' class='HQ'></h2>
                                        <h3>原価 """+str(round(all_sum/result_amount))+""" ギル</h2><h3>平均売値は """+str(search_item_average_hq) +""" ギル<br>利益 : """+str(round(search_item_average_hq-(all_sum/result_amount)))+""" ギル 利益率 : """+str(round(((search_item_average_hq-(all_sum/result_amount))/search_item_average_hq)*100)) +"""％ </h3>
                                    </div>
                                </div><div id="main_result">"""+print_data+"""</div>"""
    elif search_item_avelage_nq !=0:                                  #NQの取引履歴のみあった場合
        print_data="""<div id='result'>"""+player_info+"""
                                    <div class=icons>"""+UVS_URL+icon+"""</div>
                                    <div class=result_item>
                                        <h2>"""+item_line_Big+"""の原価は"""+str(round(all_sum/result_amount))+""" ギル。</h2>
                                        <h3>平均売値は"""+str(search_item_avelage_nq)+""" ギル<br>利益: """+str(round(search_item_avelage_nq-(all_sum/result_amount)))+""" ギル 利益率 : """+str(round((search_item_avelage_nq-(all_sum/result_amount))/search_item_avelage_nq,3)*100)+"""％ </h3>
                                    </div>
                                  </div><div id="main_result">"""+print_data+"""</div>"""
    else:                                                             #マーケットでの取り扱いがなかった場合
        print_data=player_info+"<div class='material_etc3'><h2>"+icon+"<div>"+UVS_URL+"</div>"+item_line_Big+"はマーケットでの取り扱いがありませんでした。<br>原価は "+str(round(all_sum/result_amount))+" ギル です。</h2></div>"+print_data            

    return print_data







def result_print(main_id,result_list):

    print_data=""
    all_sum=0
    search_item=get_sell(main_id)                               #完成品の販売履歴を読み込み
    search_item_average_hq=search_item[2]                       #HQの取引履歴を変数に格納
    search_item_avelage_nq=search_item[0]                       #NQの取引履歴を変数に格納

    first_floor_sum=0
    second_floor_sum=0
    third_floor_sum=0

    print_data_second_floor=""
    print_data_third_floor=""
    first_recipe=item_recipe(main_id)

    for data2 in first_recipe:
        

        first_floor_nq=0
        first_floor_hq=0

        print_data_first_floor_nq=""
        print_data_first_floor_hq=""

        first_floor_item_id=data2[0]
        first_floor_quantity=int(data2[1])

        result_data_page=search_list(result_list,first_floor_item_id)
        first_floor_item_data=result_list[result_data_page]
        first_floor_nq=first_floor_item_data[0]
        
        first_floor_hq=first_floor_item_data[2]


        first_floor_item=itemname_DB_matching(first_floor_item_id)
        first_floor_item_name=first_floor_item[2]
        first_floor_price_nq=first_floor_nq*first_floor_quantity
        first_floor_price_hq=first_floor_hq*first_floor_quantity

        first_floor_sum += first_floor_price_nq

        UVS_URL=universalis_link(first_floor_item_id)
        icon=result_image(first_floor_item_name)                            #1段目の材料アイコンを呼び出し↓へ出力
        market_icon=result_history_icon(first_floor_item_name)
        item_line1=result_tool_link(first_floor_item_name)
        


        if first_floor_hq==0:
            print_data_first_floor_hq="<h3>"+item_line1+"<img src='./static/HQicon.png' class='HQ'>の取引は確認できませんでした。</h3>"
        else:
            print_data_first_floor_hq="<h3>"+item_line1+"<img src='./static/HQicon.png' class='HQ'>"+str(first_floor_hq)+" ギル x"+str(first_floor_quantity)+" 個 = "+str(first_floor_price_hq)+" ギル</h3>"   
        if first_floor_nq==0:
            print_data_first_floor_nq="<h3>"+item_line1+"の取引は確認できませんでした。</h3>"
        else:
            print_data_first_floor_nq="<h3>"+item_line1+" "+str(first_floor_nq)+" ギル x"+str(first_floor_quantity)+" 個 = "+str(first_floor_price_nq)+" ギル</h3>"

        first_floor_item_text="""<div class=material>
                                    <div class='icon_T'>"""+UVS_URL+icon+market_icon+"""</div>
                                    """+print_data_first_floor_hq + print_data_first_floor_nq+"""
                                </div>"""
        print_data+=first_floor_item_text
        
        if item_recipe_check(first_floor_item_id)==True:
            second_recipe=item_recipe(first_floor_item_id)

            print_data_second_floor=""

            for data3 in second_recipe:
                
                
                second_floor_nq=0
                second_floor_hq=0

                print_data_second_floor_nq=""
                print_data_second_floor_hq=""

                second_floor_item_id=data3[0]
                second_floor_quantity=int(data3[1])

                second_floor_item=itemname_DB_matching(second_floor_item_id)
                second_floor_item_name=second_floor_item[2]

                result_data_page=search_list(result_list,second_floor_item_id)
                second_floor_item_data=result_list[result_data_page]
                second_floor_nq=second_floor_item_data[0]
                second_floor_price_nq=second_floor_nq*int(second_floor_quantity)
                second_floor_hq=second_floor_item_data[2]
                second_floor_price_hq=second_floor_hq*int(second_floor_quantity)

                second_floor_sum += second_floor_price_nq

                UVS_URL=universalis_link(second_floor_item_id)
                icon=result_image(second_floor_item_name)
                market_icon=result_history_icon(second_floor_item_name)
                item_line2=result_tool_link(second_floor_item_name)
                result_amount2 = int(item_recipe2(second_floor_item_id))

                if second_floor_hq==0:
                    print_data_second_floor_hq="<h3>"+item_line2+"<img src='./static/HQicon.png' class='HQ'>の取引は確認できませんでした。</h3>"
                else:
                    print_data_second_floor_hq="<h3>"+item_line2+"<img src='./static/HQicon.png' class='HQ'>"+str(second_floor_hq)+" ギル x"+str(second_floor_quantity)+" 個 = "+str(second_floor_price_hq)+" ギル</h3>"   
                if second_floor_nq==0:
                    print_data_second_floor_nq="<h3>"+item_line2+"の取引は確認できませんでした。</h3>"
                else:
                    print_data_second_floor_nq="<h3>"+item_line2+" "+str(second_floor_nq)+" ギル x"+str(second_floor_quantity)+" 個 = "+str(second_floor_price_nq)+" ギル</h3>"

                second_floor_item_text="""<div class=sub_material>
                                            <div class='icon_T'>"""+UVS_URL+icon+market_icon+"""</div>
                                            """+print_data_second_floor_hq + print_data_second_floor_nq+"""

                                        </div>"""
                
                print_data_second_floor+=second_floor_item_text
                
                if item_recipe_check(second_floor_item_id)==True:
                    third_recipe=item_recipe(second_floor_item_id)

                
                    print_data_third_floor=""

                    for data3 in third_recipe:

                        third_floor_nq=0
                        third_floor_hq=0

                        print_data_third_floor_nq=""
                        print_data_third_floor_hq=""

                        third_floor_item_id=data3[0]
                        third_floor_quantity=int(data3[1])

                        third_floor_item=itemname_DB_matching(third_floor_item_id)
                        third_floor_item_name=third_floor_item[2]

                        result_data_page=search_list(result_list,third_floor_item_id)
                        third_floor_item_data=result_list[result_data_page]
                        third_floor_nq=third_floor_item_data[0]
                        third_floor_price_nq=third_floor_nq*int(third_floor_quantity)
                        third_floor_hq=third_floor_item_data[2]
                        third_floor_price_hq=third_floor_hq*int(third_floor_quantity)

                        third_floor_sum += third_floor_price_nq

                        UVS_URL=universalis_link(third_floor_item_id)
                        icon=result_image(third_floor_item_name)
                        market_icon=result_history_icon(third_floor_item_name)
                        item_line3=result_tool_link(third_floor_item_name)
                        result_amount3 = int(item_recipe2(third_floor_item_id)) 

                        if third_floor_hq==0:
                            print_data_third_floor_hq="<h3>"+item_line3+"<img src='./static/HQicon.png' class='HQ'>の取引は確認できませんでした。</h3>"
                        else:
                            print_data_third_floor_hq="<h3>"+item_line3+"<img src='./static/HQicon.png' class='HQ'>"+str(third_floor_hq)+" ギル x"+str(third_floor_quantity)+" 個 = "+str(third_floor_price_hq)+" ギル</h3>"   
                        if third_floor_nq==0:
                            print_data_third_floor_nq="<h3>"+item_line3+"の取引は確認できませんでした。</h3>"
                        else:
                            print_data_third_floor_nq="<h3>"+item_line3+" "+str(third_floor_nq)+" ギル x"+str(third_floor_quantity)+" 個 = "+str(third_floor_price_nq)+" ギル</h3>"

                        third_floor_item_text="""<div class=sub_material>
                                                    <div class='icon_T'>"""+UVS_URL+icon+market_icon+"""</div>
                                                    """+print_data_third_floor_hq + print_data_third_floor_nq+"""
                                                </div>"""
                        
                        print_data_third_floor+=third_floor_item_text
                    

                    # result_item_price3 = round(third_floor_sum / result_amount3)

                    # if second_floor_nq == 0:
                    #     all_sum += third_floor_sum * second_floor_quantity
                    # elif result_item_price3 == 0:
                    #     all_sum += second_floor_price_nq
                    # else:
                    #     all_sum += min(second_floor_nq, result_item_price3) * second_floor_quantity

                    second_floor_sum_re=(second_floor_sum-(second_floor_nq*second_floor_quantity)+third_floor_sum)*second_floor_quantity
                    if second_floor_sum>second_floor_sum_re:
                        second_floor_sum=second_floor_sum_re



                                            
                    second_floor_item_text="""<div class='material_etc'>
                                                <h3>"""+item_line2+"""を原料から作成した場合""" +str(third_floor_sum)+"""ギル x""" +str(second_floor_quantity)+""" 個 = """+str(third_floor_sum*second_floor_quantity)+""" ギル　▼</h3>
                                            </div>"""
                    #print_data+="<details><summary>"+second_floor_item_text+"</summary>"+print_data_third_floor+"</details>"

                    print_data_second_floor=print_data_second_floor + "<details><summary>"+second_floor_item_text+"</summary>"+print_data_third_floor+"</details>"
                    third_floor_sum=0
                else:

                    pass



            result_item_price2 = round(second_floor_sum / result_amount2)

            if first_floor_nq == 0:
                all_sum += result_item_price2 * first_floor_quantity
            elif result_item_price2 == 0:
                all_sum += second_floor_price_nq
            else:
                all_sum += min(first_floor_nq , result_item_price2) * first_floor_quantity
        

            first_floor_item_text="""<div class='material_etc'>
                                        <h3>"""+item_line1+"""を原料から作成した場合""" +str(second_floor_sum)+"""ギル x""" +str(first_floor_quantity)+""" 個 = """+str(second_floor_sum*first_floor_quantity)+""" ギル　▼</h3>
                                    </div>"""
            print_data+="<details><summary>"+first_floor_item_text+"</summary>"+print_data_second_floor+"</details>"
            second_floor_sum=0

        else:

            all_sum+=first_floor_price_nq
            first_floor_sum=0

    result_amount=int(item_recipe2(main_id))
    all_sum = round(all_sum / result_amount)


    



    item_line1= result_tool_link(item_matching_id(main_id))           #検索された完成品idからボタンを作成
    item_line_Big= result_tool_link_Big(item_matching_id(main_id))    #検索された完成品idからロードストーンURLを作成
    icon=result_image_L(item_matching_id(main_id))                    #検索された完成品idから大型アイコンURLを作製
    UVS_URL=universalis_link_Big(main_id)
    player_info=read_charactor()

    if search_item_average_hq != 0:                                      #完成品のHQの取引履歴が存在した場合
        print_data="""<div id='result'>"""+player_info+"""<div class=icons>"""+UVS_URL+icon+"""</div>
                      <div class=result_item>
                        <h2>"""+item_line_Big+"""<img src='./static/HQicon.png' class='HQ'></h2>
                        <h3>原価 """+str(round(all_sum/result_amount))+""" ギル</h2><h3>平均売値は """+str(search_item_average_hq) +""" ギル<br>利益 : """+str(round(search_item_average_hq-(all_sum/result_amount)))+""" ギル 利益率 : """+str(round(((search_item_average_hq-(all_sum/result_amount))/search_item_average_hq)*100)) +"""％ </h3>
                     </div>
                     <div id="main_result">"""+print_data+"</div>"
    elif search_item_avelage_nq !=0:                                  #NQの取引履歴のみあった場合
        print_data="""<div id='result'>"""+player_info+"""<div class=icons>"""+UVS_URL+icon+"""</div>
                      <div class=result_item>
                        <h2>"""+item_line_Big+"""の原価は"""+str(round(all_sum/result_amount))+""" ギル。</h2>
                        <h3>平均売値は"""+str(search_item_avelage_nq)+""" ギル<br>利益: """+str(round(search_item_avelage_nq-(all_sum/result_amount)))+""" ギル 利益率 : """+str(round((search_item_avelage_nq-(all_sum/result_amount))/search_item_avelage_nq,3)*100)+"""％ </h3>
                      </div>
                      <div id="main_result">"""+print_data+"</div>"
    else:                                                             #マーケットでの取り扱いがなかった場合
        print_data="<div class='material_etc3'><h2>"+icon+"<div>"+UVS_URL+"</div>"+item_line_Big+"はマーケットでの取り扱いがありませんでした。<br>原価は "+str(round(all_sum/result_amount))+" ギル です。</h2></div>"+print_data            

        
    return print_data









# def result_print(main_id,result_list):


#     amount=0
#     amount2=0
#     amount3=0
    
#     sub_sum=0
#     sub_sum3=0

#     item_line1=""
#     item_line2=""
#     item_line3=""

#     result_amount=0
#     result_amount2=0

#     Sub_print_data_nq2=""
#     Sub_print_data_nq3=""

#     print_data_intermediat1=""
#     print_data_intermediat2=""

#     result_item_price2=0
#     result_item_price3=0

#     sub_print_data1=""
#     sub_print_data2=""
#     sub_print_data3=""

#     Sub_print_data_result2=""
#     Sub_print_data_result3=""
    
#     invalid_flag=False

#     all_sum=0   

#     print_data="</form><div id='sub_result'><form method='GET' action='/history'>"
#     search_item=get_sell(main_id)                               #完成品の販売履歴を読み込み
#     search_item_average_hq=search_item[2]                       #HQの取引履歴を変数に格納
#     search_item_avelage_nq=search_item[0]                       #NQの取引履歴を変数に格納


#     item_name=item_matching_id(main_id)

#     first_recipe=item_recipe(main_id)                           #完成品から必要な材料の１段目のリストを格納
#     result_amount=int(item_recipe2(main_id))                    #完成品から製作の結果生じる数を変数に格納
#     for data in first_recipe:                                   #1stレシピリストの内容を全て処理                                  
#         all_sum2=0
#         Sub_print_data_nq1=""
#         Sub_print_data_hq1=""
#         print_data_intermediat1=""
#         result_item_price2=0
#         result_average_hq=0
        
#         item_name=item_matching_id(data[0])                     #アイテム名を呼び出し
#         item_id=data[0]                                         #アイテムIDを格納
#         UVS_URL=universalis_link(item_id)                       #アイテム名、idを辞書型配列UVS_dicに格納

#         amount=int(data[1])                                     #アイテムの必要数を格納
#         result_data_page=search_list(result_list,item_id)       #全材料販売履歴リストからぴっぱりだすページを検索       
#         result_data=result_list[result_data_page]               #出力するアイテムの販売履歴リストを変数に格納
#         result_average_nq=result_data[0]                        #NQアイテムの平均値を格納
#         nq_sum=result_average_nq*amount                         #NQアイテムの平均値x必要個数＝材料の金額
#         result_average_hq=result_data[2]                        #HQアイテムの平均値を格納
#         hq_sum=result_average_hq*amount                         #HQアイテムの平均値x必要個数＝HQ材料の金額

#         item_line1=result_tool_link(item_name)                  #1段目のアイテムロードストーンリンクを作成
#         icon=result_image(item_name)                            #1段目の材料アイコンを呼び出し↓へ出力
#         market_icon=result_history_icon(item_name)
#         secand_recipe=item_recipe(data[0]) 



#         if secand_recipe==[]:
#             Sub_print_data_nq1="<div class='material_price'><div class='material_market_price'><div class='material'><div class='icon_T0'>"+UVS_URL+icon+market_icon+"</div><div class='material_etc2'><h4>"+item_line1+" "+str(result_average_nq)+" ギル x"+str(amount)+" 個 = "+str(nq_sum)+" ギル</h4></div></div></div></div>"
#             sub_print_data1+=Sub_print_data_nq1                 #1段目の素材アイテムを出力変数に格納
#             print_data+=Sub_print_data_nq1
#             Sub_print_data_nq1=""
#             sub_print_data1=""
#             #all_sum+=result_average_nq*amount                   #1段目の素材アイテムの「平均販売価格x必要数」を総合計に加算
#         else:                                                    #1段目アイテムが中間素材だった場合
#             if result_average_hq==0:
#                 Sub_print_data_hq1="<div class='clear'></div><div class=material><div class='icon_T'>"+UVS_URL+icon+market_icon+"</div><h3>"+item_line1+"<img src='./static/HQicon.png' class='HQ'>の取引は確認できませんでした。"                
#             else:
#                 Sub_print_data_hq1="<div class='clear'></div><div class=material><div class='icon_T'>"+UVS_URL+icon+market_icon+"</div><h3>"+item_line1+"<img src='./static/HQicon.png' class='HQ'>"+str(result_average_hq)+" ギル x"+str(amount)+" 個 = "+str(hq_sum)+" ギル</h3>"
#             if result_average_nq==0:
#                 Sub_print_data_nq1="<h3>"+item_line1+"の取引は確認できませんでした。</h3></div>"
#             else:
#                 Sub_print_data_nq1="<h3>"+item_line1+" "+str(result_average_nq)+" ギル x"+str(amount)+" 個 = "+str(nq_sum)+" ギル</h3></div>"
#             print_data_intermediat1=Sub_print_data_hq1+Sub_print_data_nq1       #HQの中間素材の価格と、NQの中間素材の価格の出力データを一つの変数に格納
#             second_recipe=item_recipe(item_id)                      #アイテム2段目レシピを１段目のアイテムから抽出
#             result_amount2=int(item_recipe2(item_id))               #アイテム2段目レシピの完成時の個数を抽出 
#             print_data+=print_data_intermediat1 

#             for data2 in second_recipe:                                 #2段目レシピの展開。すべて処理。                            
#                 Sub_print_data_nq2=""                                   #2段目のプリントデータnqを初期化
#                 Sub_print_data_hq2=""                                   #2段目のプリントデータhqを初期化
#                 print_data_intermediat2=""
#                 result_average_hq2=0

#                 item_id2=str(data2[0])                                  #2段目レシピのアイテムのidを格納
#                 amount2=int(data2[1])                                   #2段目レシピのアイテム必要数を格納
#                 item_name2=item_matching_id(item_id2)                   #2段目レシピのアイテム名を検索・格納

#                 UVS_URL=universalis_link(item_id2)  
                

#                 result_data_page2=search_list(result_list,item_id2)     #全材料販売履歴リストからぴっぱりだすページを検索 
#                 result_data2=result_list[result_data_page2]             #出力する販売履歴リストを変数に格納
#                 result_average_nq2=result_data2[0]                      #NQの平均販売価格を格納
#                 nq_sum2=result_average_nq2*amount2                      #NQの平均値x必要個数＝HQ材料の金額
#                 result_average_hq2=result_data2[2]                       #HQの平均販売価格を格納
#                 hq_sum2=sub_sum+int(result_data2[0])*amount2            #HQの平均値x必要個数＝HQ材料の金額
#                 if result_average_nq2==0 and result_average_hq2==0:
#                     invalid_flag=True
#                 item_line2=result_tool_link(item_name2)                 #2段目のアイテムロードストーンリンクを作成
#                 icon=result_image(item_name2)                           #2段目の材料アイコンを呼び出し↓へ出力
#                 market_icon2=result_history_icon(item_name2)
                

#                 if result_average_hq2==0:                                #2段目アイテムが素材だった場合
#                     Sub_print_data_nq2="<div class=sub_material><div class='icon_T0'>"+UVS_URL+icon+market_icon2+"</div><div class='material_etc2'><h4>"+item_line2+" "+str(result_average_nq2)+" ギル x"+str(amount2)+" 個 = "+str(nq_sum2)+" ギル</h4></div></div>"
#                     sub_print_data2+=Sub_print_data_nq2                 #2段目アイテム出力用変数にアイテムの出力データを格納            
#                 else:                                                   #2段目アイテムが中間素材だった場合
#                     Sub_print_data_hq2="<div class='clear'></div><div class=sub_material><div class='icon_T'>"+icon+market_icon2+"</div><h3>"+item_line2+"<img src='./static/HQicon.png' class='HQ'>"+str(result_average_hq2)+" ギル x"+str(amount2)+" 個 = "+str(hq_sum2)+" ギル</h3></div>"
#                     Sub_print_data_nq2="<div class=material_etc><h3>"+item_line2+" "+str(result_average_nq2)+" ギル x"+str(amount2)+" 個 = "+str(nq_sum2)+" ギル</h3></div><div class='sub_UVS'>"+UVS_URL+"</div>"
#                     print_data_intermediat2=Sub_print_data_hq2+Sub_print_data_nq2               #2段目中間素材のHQ,NQの出力を格納

#                     third_recipe=item_recipe(item_id2)                                          #3段目レシピの取得
#                     result_amount3=int(item_recipe2(item_id2))                                  #2段目中間素材の製作結果の数を格納 

#                     for data3 in third_recipe:                                                  #3段目レシピをすべて処理

#                         Sub_print_data_nq3=""                                                   #3段目のプリントデータnqを初期化。3段目は全て素材のため、hqは存在しない。

#                         item_id3=str(data3[0])                                                  #3段目レシピのアイテムのidを格納
#                         amount3=int(data3[1])                                                   #3段目レシピのアイテム必要数を格納

#                         item_name3=item_matching_id(data3[0])                                   #3段目レシピのアイテム名を検索・格納
#                         result_data_page3=search_list(result_list,item_id3)                     #全材料販売履歴リストからぴっぱりだすページを検索 
#                         result_data3=result_list[result_data_page3]                             #3段目レシピアイテムの販売履歴の検索結果を格納
#                         result_average_nq3=result_data3[0]                                      #3段目レシピのアイテム平均値x個数=金額を計算 

#                         nq_sum3=result_average_nq3*amount3
#                         sub_sum3+=int(result_average_nq3)*amount3                                  #3段目レシピ全体の合計金額を計算
#                         item_line3=result_tool_link(item_name3)                                 #3段目のアイテムロードストーンリンクを作成
#                         icon=result_image(item_name3)                                           #3段目の材料アイコンを呼び出し↓へ出力
#                         Sub_print_data_nq3="<div class='clear'></div><div class=sub_sub_material><div class='sub_icon'>"+icon+"</div><div class='material_etc2'><h4>"+item_line3+" "+str(result_average_nq3)+" ギル x"+str(amount3)+" 個 = "+str(nq_sum3)+" ギル</h4></div></div>"
#                         sub_print_data3+=Sub_print_data_nq3                                     #3段目のアイテム出力を格納
#                     result_item_price3=round(sub_sum3/result_amount3)                           #2段目の完成品の値段を算出。↓2段目の原料から～作成時のテキスト
#                     if invalid_flag==False:
#                         Sub_print_data_result3="<div class='material_etc'><h3>"+item_line2+"を原料から作成した場合" +str(result_item_price3)+"ギル x" +str(amount2)+" 個 = "+str(round(result_item_price3)*amount2)+" ギル　▼</h3></div></div>"
#                     else:
#                         Sub_print_data_result3="<div class='material_etc'><h3>"+item_line2+"はデータが不足している為、計算できませんでした。　▼</h3></div></div>"
#                     sub_sum3=0

#                 if invalid_flag==False:
#                     if result_item_price3==0:
#                         all_sum2+=(result_average_nq2*amount2)
#                     elif result_average_nq2>result_item_price3:
#                         all_sum2+=(result_item_price3*amount2)                                        #2段目合計にnqの必要数x平均金額を加算
#                     else:
#                         all_sum2+=(result_average_nq2*amount2)
#                 else:
#                     all_sum2+=(result_average_nq2*amount2)

#                 if Sub_print_data_hq2!="":                                                          #2段目が中間素材だった場合
#                     sub_print_data2+=print_data_intermediat2+Sub_print_data_result3+sub_print_data3 #出力用変数にHQ,NQの平均価格と原料から作った場合のプリントデータ、3段目のアイテム出力を足して格納
#                     sub_print_data3=""
#                 else:                                                                               #2段目が素材だった場合
#                     pass                                          #出力用変数に素材のプリントデータ（NQのみ）を格納
#                 #print_data+=Sub_print_data_result2+sub_print_data2
        
#         if all_sum2==0:                                                                         #1段目が素材だった場合
#             all_sum+=result_average_nq*amount                                                   #総合計に必要数xNQの金額を加算
#         elif result_average_nq==0:                                                              #1段目素材にNQの取引履歴が存在しない場合
#             result_item_price2+=(all_sum2/result_amount2)                                       #製作した場合の中間素材の価格を格納
#             all_sum+=(result_item_price2*amount)                                                #総合計に製作した場合の中間素材の価格x個数を格納

#         elif (all_sum2/result_amount2)>result_average_nq:                                       #中間素材を購入した方が安い場合
#             result_item_price2+=result_average_nq                                               #NQの平均価格を格納
#             all_sum+=result_average_nq*amount                                                   #総合計にNQの平均価格x個数を格納
#         elif invalid_flag==True:
#             result_item_price2+=result_average_nq                                               #NQの平均価格を格納
#             all_sum+=result_average_nq*amount                                                   #総合計にNQの平均価格x個数を格納
#         else:                                                                                   #製作した方が安い場合
#             result_item_price2+=(all_sum2/result_amount2)                                       #製作した場合の単価を格納
#             all_sum+=(result_item_price2*amount)                                                #総合計に必要数x単価を加算


#         if Sub_print_data_hq1!="":
#             if invalid_flag==False:
#                 Sub_print_data_result2="<details><summary><div class='material_etc'><h3>"+item_line1+"を原料から作成した場合" +str(round(all_sum2/result_amount2))+"ギル x" +str(amount)+" 個 = "+str(round((all_sum2/result_amount2)*amount))+" ギル　▼</h3></div></summary>"+sub_print_data2+"</details>"
#             else:
#                 Sub_print_data_result2="<details><summary><div class='material_etc'><h3>"+item_line1+"の原料からの作製単価はデータ不足により集計できませんでした。　▼</h3></div></summary>"+sub_print_data2+"</details>"
#             print_data+=Sub_print_data_result2
#         else:
#             sub_print_data1+=Sub_print_data_nq1
#             print_data+=sub_print_data1
#         sub_print_data2=""

#         invalid_flag=False

   
#     item_line1= result_tool_link(item_matching_id(main_id))           #検索された完成品idからボタンを作成
#     item_line_Big= result_tool_link_Big(item_matching_id(main_id))    #検索された完成品idからロードストーンURLを作成
#     icon=result_image_L(item_matching_id(main_id))                    #検索された完成品idから大型アイコンURLを作製
#     UVS_URL=universalis_link_Big(main_id)
#     player_info=read_charactor()

#     if search_item_average_hq != 0:                                      #完成品のHQの取引履歴が存在した場合
#         print_data=player_info+"<div class='material_etc3'><div class=icons>"+UVS_URL+icon+"</div><div class=result_item><h2>"+item_line_Big+"<img src='./static/HQicon.png' class='HQ'></h2><h2>原価 "+str(round(all_sum/result_amount))+" ギル</h2><h3>平均売値は "+str(search_item_average_hq) +" ギル<br>利益 : "+str(round(search_item_average_hq-(all_sum/result_amount)))+" ギル 利益率 : "+str(round(((search_item_average_hq-(all_sum/result_amount))/search_item_average_hq)*100)) +"％ </h3></div></div>"+print_data
#     elif search_item_avelage_nq !=0:                                  #NQの取引履歴のみあった場合
#         print_data=player_info+"<div class='material_etc3'><h2>"+icon+"<div>"+UVS_URL+"</div>"+item_line_Big+"の原価は"+str(round(all_sum/result_amount))+" ギル。</h2><h3>平均売値は"+str(search_item_avelage_nq)+" ギル<br>利益: "+str(round(search_item_avelage_nq-(all_sum/result_amount)))+" ギル 利益率 : "+str(round((search_item_avelage_nq-(all_sum/result_amount))/search_item_avelage_nq)*100)+"％ </h3></div>"+print_data
#     else:                                                             #マーケットでの取り扱いがなかった場合
#         print_data=player_info+"<div class='material_etc3'><h2>"+icon+"<div>"+UVS_URL+"</div>"+item_line_Big+"はマーケットでの取り扱いがありませんでした。<br>原価は "+str(round(all_sum/result_amount))+" ギル です。</h2></div>"+print_data            
#     print_data+="</div></form>"

#     return print_data    

def read_charactor():
    playername = request.cookies.get("char_name")  # クッキーからプレイヤー名を取得
    buy_DC = request.cookies.get("buyer_DC")  # クッキーから購入DCを取得
    buy_world = request.cookies.get("buyer_WD")  # クッキーから購入ワールドを取得  
    sell_DC = request.cookies.get("seller_DC")
    sell_WD = request.cookies.get("seller_WD")
    switchstate = request.cookies.get('switchState')

    if switchstate=="on":
        print_data="<div id=player_info><h2 id=chara_mode>キャラクター個別検索モード</h2><div class=sell_player><h2>Player:"+ playername +"</h2><h3>DC:"+sell_DC+"<br>World:"+sell_WD+"</h3></div></div><div class=buy_player><h3>購入履歴参照元DC:"+buy_DC+"<br>購入履歴参照World:"+buy_world+"</h3></div></div>"
    else:
        print_data="<div id=playerinfo><h2 id=nomal_mode>ノーマルモード</h2></div>"
    return print_data

def search_list(list,id):
    i=0
    for data in list:
        if data[4]!=id:
            i+=1
        else:
            break
    return i

def recipe_id_search(main_id):

    scan_list=[]
    scan_list2=[]
    scan_list3=[]
    list=[]

    first_recipe=item_recipe(main_id)
    if len(first_recipe)!=0:                                        #もし１段目が素材ならpass
        for data1 in first_recipe:                                  #1段目のレシピを繰り返し
            scan_list.append(data1[0])                              #スキャンリストに追加
        if len(scan_list)!=0:                                       #2段目が素材ならpass
            for data2 in scan_list:                                 #スキャンリストを繰り返し
                secand_recipe=item_recipe(data2)                    #スキャンリストからレシピを抽出
                for data3 in secand_recipe:                         #スキャンリストから抽出したレシピを繰り返し
                    scan_list2.append(data3[0])                     #スキャンリストから抽出したレシピのアイテムを登録
                    if len(scan_list2)!=0:                          #レシピが存在しない場合pass
                        for data3 in scan_list2:                    #2段目のスキャンリストを繰り返し
                            third_recipe=item_recipe(data3)      #2段目のスキャンリストからレシピを抽出
                            for data4 in third_recipe:
                                scan_list3.append(data4[0])
                                    
   
    scan_list[len(scan_list):len(scan_list)]=scan_list2
    scan_list[len(scan_list):len(scan_list)]=scan_list3

    for data in scan_list:
        if data in list:
            pass
        else:
            list.append(data)
    return list



def result_tool_link_Big(item_name):
    LDS_id=result_item_name(item_name)  
    item_line='<a href="https://jp.finalfantasyxiv.com/lodestone/playguide/db/item/'+str(LDS_id)+'/" class="eorzeadb_link">'+item_name+'</a>'
    return item_line

def result_tool_link(item_name):
    LDS_id=result_item_name(item_name)  
    item_line='<a href="https://jp.finalfantasyxiv.com/lodestone/playguide/db/item/'+str(LDS_id)+'/" class="eorzeadb_link">'+item_name+'</a>'
    return item_line


# def result_tool_link(item_name):
#     item_id=item_name_matching_id(item_name)  
#     item_line='<button class="select_history" type="submit" name="history" value="'+str(item_id)+'"><a>'+item_name+'</a></button>'
#     return item_line

def result_history_icon(item_name):
    item_id=item_name_matching_id(item_name)  
    img="<img class='market' src='./static/market.png'>"
    icon_line="<button class='market_icon'name='history' value="+str(item_id)+">"+img+"</button>"

    return icon_line


def universalis_link(item_id):
    UVS_id=item_id
    UVS_URL = '<a  target="_blank" href="https://universalis.app/market/' + str(UVS_id) + '"><img class="UVS_icon" src="./static/Universalis.png"></a>'
    return UVS_URL
    
def universalis_link_Big(item_id):
    UVS_id=item_id
    UVS_URL = '<a  target="_blank" href="https://universalis.app/market/' + str(UVS_id) + '"><img class="UVS_icon_Big" src="./static/Universalis.png"></a>'
    return UVS_URL


def result_image(item_name):
    address="https://xivapi.com"
    ItemName_DB = sqlite3.connect('ItemName_DB.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM ItemName_DB WHERE Item_Name=\'" + str(item_name) + "\'")
    list1 = c.fetchone()
    ItemName_DB.close()
    icon_address="<img class='icon' src=\""+address+list1[3]+"\">"
    return icon_address


def result_description(item_id):
    list1=[]
    description=""

    ItemName_DB = sqlite3.connect('ItemName_DB.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM ItemName_DB WHERE id=\'" + str(item_id) + "\'")
    list1 = c.fetchone()
    ItemName_DB.close()
    description=list1[6]

    return description

def result_IL(item_id):
    list1=[]
    result_IL=""

    ItemName_DB = sqlite3.connect('ItemName_DB.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM ItemName_DB WHERE id=\'" + str(item_id) + "\'")
    list1 = c.fetchone()
    ItemName_DB.close()
    result_IL=list1[4]

    return result_IL

def result_image_L(item_name):
    address="https://xivapi.com"
    ItemName_DB = sqlite3.connect('ItemName_DB.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM ItemName_DB WHERE Item_Name=\'" + str(item_name) + "\'")
    list1 = c.fetchone()
    ItemName_DB.close()
    icon_L_address=address+list1[3][:-4]+"_hr1.png"
    icon_address="<img class='iconL' src=\""+icon_L_address+"\">"

    return icon_address


def item_recipe_check(id):
    flag=False
    data=""
    recipe = sqlite3.connect('recipe.db')
    c = recipe.cursor()
    data=c.execute('SELECT * FROM Recipe WHERE field5='+str(id))  
    data=c.fetchall()    
    if len(data)==0:
        pass
    else:
        flag=True
    return flag


def item_recipe2(id):
    amount=0
    recipe = sqlite3.connect('recipe.db')
    c = recipe.cursor()
    c.execute('SELECT * FROM Recipe WHERE field5='+str(id))    
    list1=c.fetchone()
    print(list1)
    recipe.close    

    if list1 is None:
        amount=1
    else:
        amount=list1[5]
    return amount




def item_recipe(id):
    recipe_code=[]
    if int(id)>=1601:
        recipe = sqlite3.connect('recipe.db')
        c = recipe.cursor()
        c.execute('SELECT * FROM Recipe WHERE field5='+str(id))
        list1=c.fetchone()
        print(list1)
        recipe.close

        if list1 is None:
            recipe_line=[]
        else:
            for i in range(6,19,2):
                if list1[i]=='0':
                    break
                else:
                    material1=list1[i]
                    amount1=list1[i+1]
                    recipe_line=[material1,amount1]
                    recipe_code.append(recipe_line)
                    
            material1=list1[22]
            amount1=list1[23]
            recipe_line=[material1,amount1]
            recipe_code.append(recipe_line)
            if 1<=int(list1[24]):
                material1=list1[24]
                amount1=list1[25]
                recipe_line=[material1,amount1]
                recipe_code.append(recipe_line)
    else:
        pass
    return recipe_code





def result_item_name(item_name):

    ItemName_DB = sqlite3.connect('ItemName_DB.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM ItemName_DB WHERE Item_Name=\'" + str(item_name) + "\'")
    list1 = c.fetchone()
    ItemName_DB.close()
    print(list1)
    return list1[1]

def item_name_matching_id(item_name):

    ItemName_DB = sqlite3.connect('ItemName_DB.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM ItemName_DB WHERE Item_Name=\'" + str(item_name) + "\'")
    list1 = c.fetchone()
    ItemName_DB.close()
    print(list1)
    return list1[0]



def item_matching_id(id):

    ItemName_DB = sqlite3.connect('ItemName_DB.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM ItemName_DB WHERE id=" + str(id) )
    list1 = c.fetchone()
    ItemName_DB.close()
    print(list1)
    return list1[2]


def item_name_matching(itemname):

    ItemName_DB = sqlite3.connect('ItemName_DB.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM ItemName_DB WHERE Item_Name=\'" + str(itemname) + "\'")
    list1 = c.fetchone()
    ItemName_DB.close()
    print(list1)
    return list1[0]

def item_category_matching(item_category):
    item_list=[]
    ItemName_DB = sqlite3.connect('ItemName_DB.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM ItemName_DB WHERE Item_Category=\'" + str(item_category) + "\'")
    list1 = c.fetchall()
    ItemName_DB.close()
    for data in list1:
        if data[1] is None:
            pass
        else:
            id=data[0]
            LDS_id_data=data[1]
            Item_name=data[2]
            Item_icon=data[3]
            Item_Level=data[4]
            Descriprtion=data[6]
            item_line=[id,LDS_id_data,Item_name,Item_icon,Item_Level,item_category,Descriprtion]
            item_list.append(item_line)
    return item_list


def item_DB_matching(DB_name):
    item_list=[]
    ItemName_DB = sqlite3.connect('./static/DataBase/'+DB_name+'.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM Item_list")
    list1 = c.fetchall()
    ItemName_DB.close()
    for data in list1:
        if data[1] is None:
            pass
        else:
            id=data[0]
            LDS_id_data=data[1]
            Item_name=data[2]
            Item_icon=data[3]
            Item_Level=data[4]
            Item_category=data[5]
            Descriprtion=data[6]
            ClassJobCategory=data[7]
            item_line=[id,LDS_id_data,Item_name,Item_icon,Item_Level,Item_category,Descriprtion,ClassJobCategory]
            item_list.append(item_line)
    return item_list



def fc_craft_matching(select):
    fc_craft_list=[]
    if select=='1':
        category=['ホイールスタンド','ホイール']
    elif select=='2':
        category=['飛空艇：船体','飛空艇：艤装','飛空艇：船首','飛空艇：船尾','潜水艦：艦体','潜水艦：艦尾','潜水艦：艦首','潜水艦：艦橋']
    else:
        category=['外壁（一体型）']
    fc_craft_DB = sqlite3.connect('./static/DataBase/CompanyCraftSequence.db')
    c = fc_craft_DB.cursor()
    c.execute('SELECT * FROM CompanyCraftSequence')
    list1 = c.fetchall()
    fc_craft_DB.close()

    for data in list1:
        for data2 in category:
            if data[2]==data2:
                id=data[0]
                Item_name=data[1]
                Item_category=data[2]
                Item_icon=data[3]
                Item_description=data[4]
                sequence1=data[5]
                sequence2=data[6]
                sequence3=data[7]
                sequence4=data[8]
                sequence5=data[9]              
                sequence6=data[10]
                sequence7=data[11]
                sequence8=data[12]
                item_line=[id,Item_name,Item_category,Item_icon,Item_description,sequence1,sequence2,sequence3,sequence4,sequence5,sequence6,sequence7,sequence8]
                fc_craft_list.append(item_line)
    return fc_craft_list



def fc_craft_id_matching(select):
    
    item_line=[]
    fc_craft_DB = sqlite3.connect('./static/DataBase/CompanyCraftSequence.db')
    c = fc_craft_DB.cursor()
    c.execute('SELECT * FROM CompanyCraftSequence')
    list1 = c.fetchall()
    fc_craft_DB.close()

    for data in list1:
        if str(data[0])==str(select):
            id=data[0]
            Item_name=data[1]
            Item_category=data[2]
            Item_icon=data[3]
            Item_description=data[4]
            sequence1=data[5]
            sequence2=data[6]
            sequence3=data[7]
            sequence4=data[8]
            sequence5=data[9]              
            sequence6=data[10]
            sequence7=data[11]
            sequence8=data[12]
            item_line=[id,Item_name,Item_category,Item_icon,Item_description,sequence1,sequence2,sequence3,sequence4,sequence5,sequence6,sequence7,sequence8]
            break
    return item_line

def fc_craft_sequence_matching(select_list):
    process_id=""
    item_list=[]
    item_line=[]
    select=[]
    select_string=select_list[0]
    select=select_string.split(',')
    
    fc_craft_DB = sqlite3.connect('./static/DataBase/CompanyCraftProcess.db')
    c = fc_craft_DB.cursor()
    c.execute('SELECT * FROM CompanyCraftProcess')
    list1 = c.fetchall()
    fc_craft_DB.close()

    for data in select_list:
        select=data.split(',')
        for data3 in select:
            for data2 in list1:
                if data3==str(data2[0]):
                    item_list.append(data2)

    return item_list


def get_buy(search_items,crystal_flag):
    uriage_rireki = []
    histogrm={}
    result_line = []
    result_list = []
    sublist = []
    sum_price_hq = 0
    sum_price_nq = 0
    sum_quantity_hq = 0
    sum_quantity_nq = 0
    print_data_new = ""
    print_data_old = ""
    data3_line = []
    data3 = []
    sorted_data3 = []
    print_data = ""
    avelage_nq = 0
    avelage_hq = 0
    list = ""

    playername = request.cookies.get("char_name")  # クッキーからプレイヤー名を取得
    buy_DC = request.cookies.get("buyer_DC")  # クッキーから購入DCを取得
    buy_world = request.cookies.get("buyer_WD")  # クッキーから購入ワールドを取得

    if len(search_items)==1:
        search_items.append("16789")

    if crystal_flag==True:
        search_numbers=3000
    else:
        search_numbers=search_number(search_items)

    if buy_world == "All":
        buy_world = buy_DC

    for data in search_items:
        list += "," + data
    list = list[1:]

    M_get = requests.get('https://universalis.app/api/v2/history/' + str(buy_world) + '/' + str(list) + '?entriesToReturn=' + str(search_numbers))
    uriage_rireki = M_get.json()

    for data1 in search_items:
        has_history = False
        for data2 in uriage_rireki['items'][str(data1)]['entries']:
            timestamp = data2['timestamp']
            buyername = data2['buyerName']
            if buyername == playername:
                last_buy_time = timestamp
                result_line = [0, '', 0, '', data1, str(timestamp),0]
                result_list.append(result_line)
                has_history = True
                break
        if has_history == False:
            result_line = [0, '', 0, '', data1, 0, 0]
            result_list.append(result_line)

    # try:
    for data1 in search_items:
        i = 0
        for i, sublist in enumerate(result_list):
            if sublist[4] == data1:
                break
            i += 1

        for data2 in uriage_rireki['items'][str(data1)]['entries']:
            hq = data2['hq']
            price = round(data2['pricePerUnit'] * 1.05)
            quantity = data2['quantity']
            timestamp = data2['timestamp']
            buyername = data2['buyerName']
            world_name = data2['worldName']
            last_update_time = uriage_rireki["items"][str(data1)]["lastUploadTime"]
            salevelocity=uriage_rireki["items"][str(data1)]["regularSaleVelocity"]
            histogrm=uriage_rireki["items"][str(data1)]["stackSizeHistogram"]
            if buyername == playername:
                data3_line = [timestamp, hq, price, quantity, buyername, world_name]
                data3.append(data3_line)
                data3_line=[]
        total=0
        if int(data1)>=20:
            for key,value in histogrm.items():
                product=int(key)*value
                total+=product
            average_entries=total / sum(histogrm.values())
            entories_velocity=salevelocity/average_entries    
        else:
            entories_velocity=30
        sorted_data3 = sorted(data3, key=lambda x: x[0], reverse=True)            
        data3=[]
        

        if sorted_data3 != []:
            lastupdate_time = sorted_data3[0][0]
            for data in sorted_data3:               
                sorted_timestamp = data[0]
                format_timestamp=datetime.fromtimestamp(sorted_timestamp)
                sorted_hq = data[1]
                sorted_price = data[2]
                sorted_quantity = data[3]
                sorted_buyername = data[4]
                sorted_world_name = data[5]
                if datetime.fromtimestamp(lastupdate_time) - timedelta(hours=3)<= datetime.fromtimestamp(data[0]):
                    if sorted_hq == True:
                        sum_price_hq = sum_price_hq + (sorted_price * sorted_quantity)
                        sum_quantity_hq = sum_quantity_hq + sorted_quantity            
                        print_data_new = print_data_new + "<li class='hq_history'><div class='time'>" + str(format_timestamp) + "</div></div class='price'>単価: " + str(sorted_price) + "ギル</div><div class='quantity'> 購入数 : " + str(sorted_quantity).rjust(3) + "個</div><div class='buyer'>購入者 : " + sorted_buyername + "</div><div class='world'> WorldName : " + sorted_world_name + "</div></li>\n"
                    else:
                        sum_price_nq += (sorted_price * sorted_quantity)
                        sum_quantity_nq += sorted_quantity            
                        print_data_new = print_data_new + "<li class='nq_history'><div class='time'>" + str(format_timestamp) + "</div><div class='price'> 単価: " + str(sorted_price) + "ギル</div><div class='quantity'> 購入数 : " + str(sorted_quantity) + "個</div><div class='buyer'> 購入者 : " + sorted_buyername + "</div><div class='world'> WorldName : " + sorted_world_name + "</div></li>\n"
                else:   
                    print_data_old = print_data_old + "<li class='old_history'><div class='time'>" + str(format_timestamp) + "</div><div class='price'> 単価: " + str(sorted_price) + "ギル</div><div class='quantity'> 購入数 : " + str(sorted_quantity) + "個</div><div class='buyer'> 購入者 : " + sorted_buyername + "</div><div class='world'> WorldName : " + sorted_world_name + "</div></li>\n"
            sorted_data3=[]
            if sum_price_hq != 0:
                avelage_hq = round(sum_price_hq / sum_quantity_hq)
            else:
                avelage_hq = 0
            if sum_price_nq != 0:
                avelage_nq = round(sum_price_nq / sum_quantity_nq)
            else:
                avelage_nq = 0

            print_data = print_data_new + print_data_old
            result_list[i] = [avelage_nq, print_data, avelage_hq, '', data1, lastupdate_time,entories_velocity]
            SUM_list = [data, sum_price_hq, sum_quantity_hq, sum_price_nq, sum_quantity_nq, last_update_time]

            print_data = ""
            print_data_new=""
            print_data_old=""
            sum_price_hq = 0
            sum_quantity_hq = 0
            sum_price_nq = 0
            sum_quantity_nq = 0
            avelage_hq = 0
            avelage_nq = 0
            result_list
    return result_list

    # except(KeyError):
    #     result_list = [0, 0, 0, 0, data1]
    #     return result_list
   




def get_buy_all(search_items):
    uriage_rireki = []
    histogrm={}
    result_list = []
    sum_price_hq = 0
    sum_price_nq = 0
    sum_quantity_hq = 0
    sum_quantity_nq = 0
    print_data_new = ""
    print_data_old = ""
    data3_line = []
    data3 = []
    sorted_data3 = []
    print_data = ""
    avelage_nq = 0
    avelage_hq = 0
    list = ""
    sorted_and_cut=[]

    buy_DC = request.cookies.get("buyer_DC")  # クッキーから購入DCを取得
    buy_world = request.cookies.get("buyer_WD")  # クッキーから購入ワールドを取得

    if len(search_items)==1:
        search_items.append("16789")

    search_numbers=20

    if buy_world == "All":
        buy_world = buy_DC

    for data in search_items:
        list += "," + data
    list = list[1:]

    M_get = requests.get('https://universalis.app/api/v2/history/' + str(buy_world) + '/' + str(list) + '?entriesToReturn=' + str(search_numbers))
    uriage_rireki = M_get.json()

    for data1 in search_items:
        i = 0

        for data2 in uriage_rireki['items'][str(data1)]['entries']:
            hq = data2['hq']
            price = round(data2['pricePerUnit'] * 1.05)
            quantity = data2['quantity']
            timestamp = data2['timestamp']
            buyername = data2['buyerName']
            world_name = data2['worldName']
            last_update_time = uriage_rireki["items"][str(data1)]["lastUploadTime"]
            salevelocity=uriage_rireki["items"][str(data1)]["regularSaleVelocity"]
            histogrm=uriage_rireki["items"][str(data1)]["stackSizeHistogram"]
            data3_line = [timestamp, hq, price, quantity, buyername, world_name]
            data3.append(data3_line)
        sorted_data3 = sorted(data3, key=lambda x: x[2])
        data3=[]
        
        total=0
        if int(data1)>=20:
            for key,value in histogrm.items():
                product=int(key)*value
                total+=product
            average_entries=total / sum(histogrm.values())
            entories_velocity=salevelocity/average_entries    
        else:
            entories_velocity=30

        for i in range(0,20):
            sorted_and_cut.append(sorted_data3[i])

        for data in sorted_and_cut:
            sorted_price = 0
            sorted_quantity = 0               
            sorted_timestamp = data[0]
            format_timestamp=datetime.fromtimestamp(sorted_timestamp)
            sorted_hq = data[1]
            sorted_price = data[2]
            sorted_quantity = data[3]
            sorted_buyername = data[4]
            sorted_world_name = data[5]
            if sorted_hq == True:
                sum_price_hq = sum_price_hq + (sorted_price * sorted_quantity)
                sum_quantity_hq = sum_quantity_hq + sorted_quantity            
                print_data_new = print_data_new + """<li class='hq_history'>
                                                        <div class='time'>""" + str(format_timestamp) + """</div>
                                                        <div class='price'>単価: """ + str(sorted_price) + """ギル</div>
                                                        <div class='quantity'> 購入数 : """ + str(sorted_quantity).rjust(3) + """個</div>
                                                        <div class='buyer'>購入者 : """ + sorted_buyername + """</div>
                                                        <div class='world'> WorldName : """ + sorted_world_name + """</div>
                                                    </li>"""
            else:
                sum_price_nq += (sorted_price * sorted_quantity)
                sum_quantity_nq += sorted_quantity            
                print_data_new = print_data_new + """<li class='nq_history'><div class='time'>""" + str(format_timestamp) + """</div>
                                                        <div class='price'> 単価: """ + str(sorted_price) + """ギル</div>
                                                        <div class='quantity'> 購入数 : """ + str(sorted_quantity) + """個</div>
                                                        <div class='buyer'> 購入者 : """ + sorted_buyername + """</div>
                                                        <div class='world'> WorldName : """ + sorted_world_name + """</div>
                                                    </li>"""
        sorted_and_cut=[]
        if sum_price_hq != 0:
            avelage_hq = round(sum_price_hq / sum_quantity_hq)
        else:
            avelage_hq = 0
        if sum_price_nq != 0:
            avelage_nq = round(sum_price_nq / sum_quantity_nq)
        else:
            avelage_nq = 0
            
        print_data = print_data_new + print_data_old
        result_line= [avelage_nq, print_data_new, avelage_hq, '', data1, last_update_time,entories_velocity]
        result_list.append(result_line)
        result_line=[]

        sorted_hq = False
        sorted_price = 0
        sorted_quantity = 0
        sorted_buyername = ""
        sorted_world_name = ""

        print_data = ""
        print_data_new=""
        print_data_old=""
        sum_price_hq = 0
        sum_quantity_hq = 0
        sum_price_nq = 0
        sum_quantity_nq = 0
        avelage_hq = 0
        avelage_nq = 0
        result_list
    return result_list

    # except(KeyError):
    #     result_list = [0, 0, 0, 0, data1]
    #     return result_list




def search_number(search_items):

    max=1
    dt_now=datetime.now()
    time_max = dt_now.timestamp()
    sell_velocity=1
    lastupdate=time_max
    for data in search_items:
        cookie_value = request.cookies.get(data)  # data[4]をクッキー名として指定        
        if cookie_value is not None:
            cookie_parts = cookie_value.split(',')
            if cookie_parts[0]!="0": 
                if int(cookie_parts[3])!=0:         
                    lastupdate = int(cookie_parts[3])
                    if time_max>lastupdate:
                        time_max=lastupdate
                    sell_velocity=float(cookie_parts[4])
                    if max<sell_velocity:
                        max=sell_velocity
            else:
                sell_velocity=30
            
            
    if time_max==dt_now.timestamp():
        search_numbers=3000
    else:
        dt_now=datetime.now()
        timestamp_max = datetime.fromtimestamp(time_max)
        days_elapsed=(dt_now-timestamp_max).days
        if days_elapsed==0:
            days_elapsed=3
        search_numbers_f=days_elapsed*max
        search_numbers=int(round(search_numbers_f))

    return search_numbers


def get_sell(search_item):
    uriage_rireki=[]
    result=[]
    sum_price_hq=0
    sum_price_nq=0
    sum_quantity_hq=0
    sum_quantity_nq=0
    print_data_hq=""
    print_data_nq=""
    avelage_nq=0
    avelage_hq=0

    M_get=requests.get('https://universalis.app/api/v2/history/tonberry/'+search_item+'?entriesToReturn=3')
    uriage_rireki=M_get.json()
    try:
        for data2 in uriage_rireki['entries']:
            hq=data2['hq']
            price=data2['pricePerUnit']
            quantity=data2['quantity']
            timestamp=data2['timestamp']
            buyername=data2['buyerName']
            timestamp_format = datetime.fromtimestamp(timestamp)
            if hq==True:
                sum_price_hq = sum_price_hq + (price*quantity)
                sum_quantity_hq = sum_quantity_hq + quantity            
                print_data_hq+="<li>"+str(timestamp_format)+" 単価: "+ str(price) +"ギル 購入数 : " +str(quantity)+ "個 購入者 : " + buyername+"</li>\n"
            else:
                sum_price_nq += (price*quantity)
                sum_quantity_nq += quantity            
                print_data_nq += "<li>"+str(timestamp_format)+" 単価: "+ str(price) +"ギル 購入数 : " +str(quantity)+ "個 購入者 : " + buyername+"</li>\n"

        if sum_price_hq!=0:
            avelage_hq=round(sum_price_hq/sum_quantity_hq)
        else: avelage_hq=0
        if sum_price_nq!=0:
            avelage_nq=round(sum_price_nq/sum_quantity_nq)
        else:
            avelage_nq=0
        result=[avelage_nq,print_data_nq,avelage_hq,print_data_hq,search_item]
        print_data_nq=""
        print_data_hq=""
        sum_price_hq=0
        sum_quantity_hq=0
        sum_price_nq=0
        sum_quantity_nq=0
        avelage_hq=0
        avelage_nq=0
        return result

    except(KeyError):
        result=[0,0,0,0,search_item]
    return result    



def get_history(search_item):
    uriage_rireki=[]
    result_line=[]
    search=0
    sum_price_hq=0
    sum_price_nq=0
    sum_quantity_hq=0
    sum_quantity_nq=0
    print_data=[]
    avelage_nq=0
    avelage_hq=0
    list=""

    world_list=['Aegis','Atomos','Carbuncle','Garuda','Gungnir','Kujata','Tonberry','Typhon',
                'Alexander','Bahamut','Durandal','Fenrir','Ifrit','Ridill','Tiamat','Ultima',
                'Anima','Asura','Chocobo','Hades','Ixion','Masamune','Pandaemonium','Titan',
                'Belias','Mandragora','Ramuh','Shinryu','Unicorn','Valefor','Yojimbo','Zeromus',
                'Adamantoise','Cactuar','Faerie','Gilgamesh','Jenova','Midgardsormr','Sargatanas','Siren',
                'Balmung','Brynhildr','Coeurl','Diabolos','Goblin','Malboro','Mateus','Zalera',
                'Halicarnassus','Maduin','Marilith','Seraph',
                'Behemoth','Excalibur','Exodus','Famfrit','Hyperion','Lamia','Leviathan','Ultros',
                'Cerberus','Louisoix','Moogle','Omega','Phantom','Ragnarok','Sagittarius','Spriggan',
                'Alpha','Lich','Odin','Phoenix','Raiden','Shiva','Twintania','Zodiark',
                'Bismarck','Ravana','Sephirot','Sophia','Zurvan'
                ]

    playername = request.cookies.get("char_name")  # クッキーからプレイヤー名を取得
    buy_DC = request.cookies.get("buyer_DC")  # クッキーから購入DCを取得
    buy_world = request.cookies.get("buyer_WD")  # クッキーから購入ワールドを取得    

    if buy_world in world_list:
        search=5000
    else:
        search=50000



    M_get=requests.get('https://universalis.app/api/v2/history/'+str(buy_world)+'/'+str(list)+'?entriesToReturn='+str(search))
    uriage_rireki=M_get.json()
    try:
        for data2 in uriage_rireki['items'][str(search_item)]['entries']:
            hq=data2['hq']
            price=data2['pricePerUnit']*1.05
            quantity=data2['quantity']
            timestamp=data2['timestamp']
            buyername=data2['buyerName']
            if buyername==playername:
                print_data.append[hq,timestamp,price,quantity,buyername]

        return print_data

    except(KeyError):
        result_line=[0,0,0,0,0]
    return result_line    

def itemname_DB_matching(id):

    ItemName_DB = sqlite3.connect('ItemName_DB.db')
    c = ItemName_DB.cursor()
    c.execute("SELECT * FROM ItemName_DB WHERE id=" + str(id) )
    list1 = c.fetchone()
    ItemName_DB.close()
    print(list1)
    return list1



if __name__=='__main__':
   app.debug=True
   app.run(host='localhost')
   app.run(debug=True)

