package="com.taobao.taobao";
activity="com.taobao.search.searchdoor.SearchDoorActivity";

//activity="com.taobao.search.searchdoor.MultipleSearchDoorActivity";

var vol=device.getMusicVolume()
device.setMusicVolume(0)
// mute the thing please?

app.startActivity({action:"View",
packageName:package,className:activity,
root:true,
//category:["com.taobao.intent.category.search.MULTI_SEARCHDOOR"],
data:"http://s.m.taobao.com/...",})
 // not launching 淘宝逛逛
 
 /*
 
 2221:2022-11-02 13:02:20.328 | startActivity { calling=com.taobao.taobao:-1--1, rc=10159-1987, iTS=false, requestCode=-1, startFlags=0, target=com.taobao.taobao/com.taobao.search.searchdoor.SearchDoorActivity<true>, intent=Intent { act=android.intent.action.VIEW dat=http://s.m.taobao.com/... pkg=com.taobao.taobao cmp=com.taobao.taobao/com.taobao.search.searchdoor.SearchDoorActivity (has extras) }, extras={ NAV_START_ACTIVITY_TIME:(java.lang.Long)1667365340316, ad_type:(java.lang.String)1.0, NAV_TO_URL_START_TIME:(java.lang.Long)1667365340268, referrer:(java.lang.String)http://market.m.taobao.com/app/tb-source-app/video-fullpage/pages/index2?wh_weex=false&wx_navbar_transparent=true&wx_navbar_hidden=true&id=380201806724&bizParameters=%7B%22itemIds%22%3A%22681366994883%22%2C%22contentId%22%3A%22380201806724%22%2C%22videoId%22%3A%22380201806724%22%7D&videoUrl=http%3A%2F%2Fcloud.video.taobao.com%2Fplay%2Fu%2F2208882892036%2Fp%2F1%2Fe%2F6%2Ft%2F1%2F380201806724.mp4&type=cainixihuansy&source=cainixihuansy&business_spm=a211r6.cjvideo&hideAccountInfo=false&extParams=%7B%2288_bucket%22%3A%220%22%7D&scm=1007.10088.311498.0&spm=a2141.1.guessitemtab_1.5&pvid=b9ca1499-6a25-4913-9b4a-a2c703576f45&utparam=%7B%22x_sid%22%3A%2252aa36213ede47006361f9b21dbc602d%22%2C%22card_subtype%22%3A%22xgc%22%2C%22up_pvid%22%3A%22f88bbfa6-c859-44a5-94bb-e0599c889e5a%22%2C%22x_sid_cpm%22%3A%22be353521ca7fc7006361f9b20c542845%22%2C%22x_object_type%22%3A%22VIDEO_916%22%2C%22x_ad_bucketid_cpm%22%3A%2212676854%2C17296858%22%2C%22hybrid_score%22%3A0.303358%2C%22x_biz%22%3A%22VIDEO_916%22%2C%22sessionid%22%3A%22b9ca1499-6a25-4913-9b4a-a2c703576f45%22%2C%22tpp_buckets%22%3A%22%7E9%7EU2wG6g9N1IaCq1M7J1Ia11K6A2Tg4x4I02E6nIfMi-u9KM9NveH1FhPjhxK7AniKCnO3mIO8Kj2dCQ6NhoMCwioGO1X6ddGN2W5qOUcWe41W2PePv31PMlSe11O2XcVr31EA5_s41zO2NubdRr-Z851Q1I7Li2dFU4S93dGSkxl5dU2TcFf7dBN8Cf8d_2ImFqbdY2A1JvbdM1U1P3cdX1y4IlcdZ1L6w9ddyCN9ddBN9AeedJL7Htgd_2Qpx2jdCW2QgjdzC4w2kdDJ8B6ldF%7EwpwFaf9z%7EZb7wWs29B%7EJhwQ4f9-B22y65-1Gp2BfmB2%7EGdwGfh9O1K52Nj5GSg2RplCB4V3mIN61FhfdIGcW041AEuHshdEDn1Lj7dFY5y98dB1O4H29dz-hw3cdPL1MqbdDVj1V4mdZ2C1WfkdFEp-4mdOF1IemdU%7EXk1wC0d9G%7EPi3wJh59wNeUo1Xp%7Ezv1wYcn5wEt7Uv2dD2C7Li3dGqKuQp7dU4zk1AcedZ4W7W0idRp%7EWecwFq49HPt8Dv9dNZ82U8gdKNqS6kdQWIbkdYU4VskdQ%7EFt4wG8g9A%22%2C%22miniapphc_score%22%3A0.0%2C%22x_summary_trackInfo%22%3A%22380569870474---380569870474-new_vp_4_3-new_vp_4_3%22%2C%22pvid%22%3A%22b9ca1499-6a25-4913-9b4a-a2c703576f45%22%2C%22evo_buckets%22%3A%22evo263227_118977%23275047_321220%23286254_324141%23337973_477247evo%22%2C%22auction_score%22%3A0.0%2C%22scm%22%3A%221007.10088.311498.428654_37338_4631_438253_439584_428623_446528_434662_23752_438956_34262_433641_443307_25137_36851_22642_38173_25152_431777_445505_440772_438225_439515_37791_36729_1862_34124_26810_438089_445972_429366_447685_15345_10206_438387_19172_18035_439601%22%2C%22glc%22%3A%221%22%2C%22guessModelVersion%22%3A%2220211016%22%2C%22mtx_c%22%3A380201806724%2C%22matrix_score%22%3A0.0%2C%22miniapp_score%22%3A0.0%2C%22card_type%22%3A%22xgc%22%2C%22x_item_ids%22%3A%22681366994883%22%2C%22author_id%22%3A%222208882892036%22%2C%22guess_buckets%22%3A%226595_11513_11609_12894_13440_17348_19178_21337_21230_20634_22262%22%2C%22x_sytab%22%3A%221001%22%2C%22x_object_id%22%3A380201806724%7D&itemid=681366994883&item_id=681366994883&noDynamicRec=1&newItemList=1&utabtest=aliabtest184572_25123, URL_REFERER_ORIGIN:(java.lang.String)//s.m.taobao.com/h5entry?g_channelSrp=videointeract&g_tab=tbexperience&g_pfilter=daren&g_closeModues=tab&closeExpSubTab=true&g_csearchdoor_spm=a310p.14955560&spm=a310p.13800399&launchMode=android_new_task&g_closeExpSubTab=true, WEEX_NAV_PROCESSOR_TIME:(java.lang.Long)1667365340292 } }.../xintent/logs #
 
 */
 
 waitForPackage(package);
 //跳转之后可能出现过期的提示
 //可能需要轮询

 for (var i=0;i<5;i++){//triple check?
 while (true){
     sleep(200);
  var succ=click("我知道了");
  if (succ){break;}
 if (currentActivity() ==activity)break;
 }
 }
 mytext="【淘宝】https://m.tb.cn/h.UfbOyIi?sm=26a80a?tk=XjXUd0OFtMN CZ0001 「这就是：我预判了你的预判吗」点击链接直接打开"
 setText(mytext)
 
 //淘宝直接输入到搜索框里面 然后用这个进入视频搜索界面
 while(!click("搜索"));
 
waitForActivity("com.taobao.android.interactive.timeline.VideoListActivity2")

id("imgSearch").findOne().click()

waitForActivity("com.taobao.search.searchdoor.MultipleSearchDoorActivity")
setText("猫猫")

//Text("猫猫")

while(!click("搜索"));

//可能出现搜索失败的情况 请注意

device.setMusicVolume(vol)