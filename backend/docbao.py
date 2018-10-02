#####################################################################################################################
#Program: Doc bao theo tu khoa (keyword-based online journalism reader)
#Author: hailoc12
#Version: 1.9
#Date: 2/10/2018 (Oct, 2nd 2018)
#Repository: http://github.com/hailoc12/docbao
#Donation is welcomed if you feel this program useful
#Bank: Vietcombank (Vietnam)
#Account: DANG HAI LOC
#Number: 0491000010179
#####################################################################################################################

# IMPORT LIB
import xlsxwriter
from _class._class import *
from _class._utility import *
import jsonpickle
import sys
# CHECK IF ANOTHER SESSION IS RUNNING
if is_another_session_running():
    print("ANOTHER SESSION IS RUNNING !")
    print("If you believe this is error, please delete docbao.lock file")
    exit()
else:
    new_session()

# GLOBAL OBJECT
config_manager = ConfigManager(get_independent_os_path(['input', 'config.txt'])) #config object
data_manager = ArticleManager(config_manager, get_independent_os_path(["data", "article.dat"]),get_independent_os_path(["data","blacklist.dat"]) ) #article database object
keyword_manager = KeywordManager(data_manager, config_manager, get_independent_os_path(["data", "keyword.dat"]), get_independent_os_path(["input", "collocation.txt"]), get_independent_os_path(["input", "keywords_to_remove.txt"]))    #keyword analyzer object

def export_result():

    # export database in excel format

    workbook = xlsxwriter.Workbook(get_independent_os_path(["export", "csdl_bao_chi_ngay_" + datetime.now().strftime("%d-%m-%Y") + '.xlsx']))
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "STT")
    worksheet.write(0, 1, "Bài viết")
    worksheet.write(0, 2, "Link")
    worksheet.write(0, 3, "Báo")
    worksheet.write(0, 4, "Ngày xuất bản")
    worksheet.write(0, 5, "Sapo")
    row = 1
    col = 0

    count = 0
    for article in data_manager.get_sorted_article_list():
        count+=1
        worksheet.write(row, col, count )
        worksheet.write(row, col+1, article.get_topic())
        worksheet.write(row, col+2, article.get_href())
        worksheet.write(row, col+3, article.get_newspaper())
        worksheet.write(row, col+4, article.get_date())
        worksheet.write(row, col+5, article.get_summary())
        row+=1
    workbook.close()

    # local frontend as index.html file
    html_begin = '''<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    <style>
    a:link    {
      /* Applies to all unvisited links */
      text-decoration:  none;
      } 
    a:visited {
      /* Applies to all visited links */
      text-decoration:  none;
      } 
    a:hover   {
      /* Applies to links under the pointer */
      text-decoration:  underline;
      } 
    a:active  {
      /* Applies to activated links */
      text-decoration:  underline;
      } 
    table {
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                }

                td, th {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }

                tr:nth-child(even) {
                    background-color: #dddddd;
                }

                #myInput {
                    background-image: url('https://www.w3schools.com/css/searchicon.png'); /* Add a search icon to input */
                    background-position: 10px 12px; /* Position the search icon */
                    background-repeat: no-repeat; /* Do not repeat the icon image */
                    width: 100%; /* Full-width */
                    font-size: 16px; /* Increase font-size */
                    padding: 12px 20px 12px 40px; /* Add some padding */
                    border: 1px solid #ddd; /* Add a grey border */
                    margin-bottom: 12px; /* Add some space below the input */
                }

                #myTable {
                    border-collapse: collapse; /* Collapse borders */
                    width: 100%; /* Full-width */
                    border: 1px solid #ddd; /* Add a grey border */
                    font-size: 18px; /* Increase font-size */
                }

                #myTable th, #myTable td {
                    text-align: left; /* Left-align text */
                    padding: 12px; /* Add padding */
                }

                #myTable tr {
                    /* Add a bottom border to all table rows */
                    border-bottom: 1px solid #ddd; 
                }

                #myTable tr.header, #myTable tr:hover {
                    /* Add a grey background color to the table header and on hover */
                    background-color: #f1f1f1;
                }
                #keyword
                {
                  color: blue;
                  background-color: #f1f1f1; 
                }
    </style>
    <script>
                function showArticle() {
                  // Declare variables 
                  var input, filter, table, tr, td, i;
                  input = document.getElementById("myInput");
                  filter = input.value.toUpperCase();
                  table = document.getElementById("myTable");
                  tr = table.getElementsByTagName("tr");
                  // re_str = "(\\\\\s+"+filter+"\\\\\s+)"+"|(^"+filter+"\\\\\s+)"+"|(\\\\\s+"+filter+"$)"; 
                  // re = new RegExp(re_str, 'i');
                  // console.log(re_str)
                  // console.log(re)
                    
                  // Loop through all table rows, and hide those who don't match the search query
                  for (i = 0; i < tr.length; i++) 
                  {
                    td = tr[i].getElementsByTagName("td")[1];
                    if (td) 
                    {
                      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                          } 
                        else {
                            tr[i].style.display = "none";
                          }
                    } 
                  }
                }
                
                function clickKeyword(object)
                {
                	document.getElementById("myInput").value = object.innerHTML;
                	showArticle();
                }
                
                function showNewspaper(object)
                {
                  table = document.getElementById("myTable");
                  tr = table.getElementsByTagName("tr");
                  filter = object.value.toUpperCase();                    
                  // Loop through all table rows, and hide those who don't match the search query
                  for (i = 0; i < tr.length; i++) 
                  {
                    td = tr[i].getElementsByTagName("td")[2];
                    if (td) 
                    {
                      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) 
                      {
                        if(object.checked) 
                        {
                        tr[i].style.display = ""; 
                        
                        } 
                        else 
                        {
                           tr[i].style.display = "none";
                        }
                      } 
                    }
                  }
                  //showArticle();
                }
                
                function uncheck_all_newspaper_checkbox()
                {
                    checkboxes = document.getElementById("newspaper_checkbok");
                    for(i=0; i<checkboxes.length; i++)
                    {
                        checkboxes[i].checked = false;
                    }
                }
                
                function uncheck_all_newspaper_checkbox_except_this(object)
                {
                    checkboxes = document.getElementById("newspaper_checkbok");
                    for(i=0; i<checkboxes.length; i++)
                    {
                        if (checkboxes[i].value != this.value)
                        {
                            checkboxes[i].checked = false;
                        }
                        else
                        {
                            checkboxes[i].checked = true;
                        }
                        
                    }
                }
            </script>
    </head>
    <body>
    '''
    html_end = '''
        <script>
            (function(w,d,t,u,n,a,m){w['MauticTrackingObject']=n;
                w[n]=w[n]||function(){(w[n].q=w[n].q||[]).push(arguments)},a=d.createElement(t),
                m=d.getElementsByTagName(t)[0];a.async=1;a.src=u;m.parentNode.insertBefore(a,m)
            })(window,document,'script','https://www.campaign.tudonghoamaytinh.com/mtc.js','mt');
        
            mt('send', 'pageview');
        </script>
        </body>
        </html>
        '''

    with open_utf8_file_to_write(get_independent_os_path(["export", "local_html", "index.html"])) as stream:
        stream.write(html_begin)
        stream.write("<h1> ĐỌC BÁO THEO TỪ KHÓA </h1>")
        stream.write("<h4> Cập nhật: " + datetime.now().strftime("%d/%m/%Y %H:%M") +
                     "</h4>")
        stream.write("<h4>Trích tự động từ " + str(config_manager.get_newspaper_count()) + " trang báo với " + str(
            data_manager.count_database()) + " bài xuất bản trong ngày hôm nay." +
                     " Click để đọc</h4>")
        # write hot tag list

        # write keyword list to json file
        keyword_manager.write_trending_keyword_to_json_file()
        keyword_manager.write_keyword_dicts_to_json_files()
        #tag_extract.write_tag_dict_to_file() # to create word cloud
        #tag_extract.write_hot_keyword_to_text_file() # to create facebook status

        stream.write('<table>')
        stream.write('<a name="keyword_table"></a>')
        stream.write("<tr>")
        stream.write("<th>Chuyên mục</th>")
        stream.write("<th>Keyword nổi bật</th>")
        stream.write("</tr>")
        for category in config_manager.get_categories():
            stream.write("<tr>")
            stream.write("<td>" + category.get_name() + "</td>")
            tag_string = ""
            for keyword, count in keyword_manager.get_hot_keyword_dict_by_category(category).items():
                if keyword != '': # chua biet tai sao lai co ca tag trang
                    tag_string = tag_string + '<a href="#article_table">''<font size="' + str(count/6+3) + \
                                 'px"' + '>' + \
                                 '<span id="keyword" onclick="clickKeyword(this)">' + keyword  + '</span>' +  \
                                 '<font size="2">' + "<sub>" + str(count) + "</sub>" "</font>" + "</font>" + '</a>' +"   •   "
            stream.write("<td>")
            stream.write(tag_string)
            stream.write("</td>")
            stream.write("</tr>")
        stream.write('</table>')
        stream.write('<br>')

        keyword_manager.write_uncategoried_keyword_to_text_file() # for crowdsource
        # search input
        stream.write("<p>Lọc bài theo từ khóa của bạn:")
        stream.write('<input type="text" id="myInput" onkeyup="showArticle()" placeholder="Lọc bài báo theo từ khóa của bạn"></p>')

        stream.write("<p>Lọc tiếp bài theo nguồn báo (nếu cần)")
        stream.write("</br>")
        for newspaper in config_manager.get_newspaper_list():
            stream.write('<input type="checkbox" id="newspaper_checkbok" value= "' + newspaper.get_webname() +
                         '" onchange = "showNewspaper(this)" checked>' +
                         "   " + newspaper.get_webname() + "   " + '</input>')
        stream.write('</br>')
        stream.write('<input type="button" onclick="uncheck_all_newspaper_checkbox()" value="Bỏ chọn tất cả"></input>')
        stream.write("</p>")

        stream.write('<p><h5><i>Hãy góp sức <a href="http://docbao.tudonghoamaytinh.com/update_csdl.html" target="_blank">bổ sung thêm từ khóa'
                     '</a> hoặc <a href="http://docbao.tudonghoamaytinh.com/display_category.php">phân nhóm chuyên mục cho từ khóa</a> '
                     'để hệ thống phục vụ cộng đồng hiệu quả hơn</i></h5></p>')


        stream.write('<a href="#keyword_table">Trở về đầu trang </a>')

        stream.write("<br>")


        stream.write('<table id="myTable">')
        stream.write('<a name="article_table"></a>')
        stream.write("<tr>")
        stream.write("<th>STT</th>")
        stream.write("<th>Bài</th>")
        stream.write("<th>Báo</th>")
        stream.write("<th>Cập nhật</th>")
        stream.write("<th>Ngày xuất bản</th>")
        stream.write("</tr>")

        json_article_list=[]
        count = 0
        for article in data_manager.get_sorted_article_list():
            count += 1
            stream.write("<tr>")
            stream.write("<td>" + str(count) + "</td>")
            stream.write("<td>" + '<a href="' + article.get_href() + '"' + 'target="_blank">' + article.get_topic() + "</a></td>")
            stream.write("<td>" + article.get_newspaper() +"</td>")
            update_time = int((datetime.now() - article.get_creation_date()).total_seconds() / 60)
            if update_time >= 720:
                update_time = int(update_time / 720)
                update_time_string = str(update_time) + " ngày trước"
            else:
                if update_time >= 60:
                    update_time = int(update_time / 60)
                    update_time_string = str(update_time) + " giờ trước"
                else:
                    update_time_string = str(update_time) + " phút trước"

            stream.write("<td>" + update_time_string + "</td>")
            stream.write("<td>" + article.get_date()+"</td>")
            stream.write("</tr>")

            json_article_list.append({'stt':str(count),'topic':article.get_topic(),'href':article.get_href(),
                                      'newspaper': article.get_newspaper(),'update_time': update_time_string,
                                      'publish_time': article.get_date()})
        stream.write("</table>")

        stream.write(html_end)
    stream.close()
    # export article database to json file
    with open_utf8_file_to_write(get_independent_os_path(["export", "article_data.json"])) as stream:
        stream.write(jsonpickle.encode({'article_list': json_article_list}))
    stream.close()
    # in keyword freq series to json file
    keyword_manager.write_keyword_freq_series_to_json_file()

def write_log_data_to_json():
    with open_utf8_file_to_write(get_independent_os_path(["export", "log_data.json"])) as stream:
        log_dict = dict()
        log_dict['update_time'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        log_dict['newspaper_count'] = str(config_manager.get_newspaper_count())
        log_dict['database_count'] = str(data_manager.count_database())
        stream.write(jsonpickle.encode(log_dict))
        stream.close()


#MAIN PROGRAM
#init data
config_manager.load_data()
data_manager.load_data()
keyword_manager.load_data()

#console output
version = "1.9.0"
print("DOC BAO VERSION " + version + "       Days to crawl: " + str(config_manager.get_maximum_day_difference()+1))

#compress database
data_manager.compress_database(keyword_manager)
data_manager.compress_blacklist()

#crawling data
print("PHASE I: CRAWLING DATA")
for webconfig in config_manager.get_newspaper_list():
    data_manager.add_articles_from_newspaper(webconfig)

print("Number of articles in database: " + str(data_manager.count_database()))
print("Number of link in blacklist database: " + str(data_manager.count_blacklist()))

#analyze keyword
print("PHASE II: ANALYZE KEYWORDS FROM ARTICLE DATABASE")
print("")
keyword_manager.build_keyword_list()

#export data
print("PHASE III: EXPORT DATA IN EXCEL, HTML, JSON FORMAT")

export_result()
write_log_data_to_json()

print("PHASE IV: SAVE DATA")
#luu du lieu
data_manager.save_data()
keyword_manager.save_data()

print("FINISH")
# clear lock file to finish this session
finish_session()
