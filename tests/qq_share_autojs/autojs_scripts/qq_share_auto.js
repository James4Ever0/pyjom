auto();

var cmd = "am start -S -n com.tencent.mobileqq/com.tencent.mobileqq.activity.JumpActivity -a android.intent.action.VIEW -d 'mqqapi://share/to_fri?src_type=app&version=1&file_type=news&file_data=L3N0b3JhZ2UvZW11bGF0ZWQvMC9QaWN0dXJlcy9zaGFyZS9jYXQuZ2lm&file_uri=ZmlsZTovLy9zdG9yYWdlL2VtdWxhdGVkLzAvUGljdHVyZXMvc2hhcmUvY2F0LmdpZg%3D%3D&title=5ZOU5ZOp5ZOU5ZOp&description=5Za15Za15Za1&share_id=100951776&url=aHR0cHM6Ly9iMjMudHYvdUhNTDVtaQ%3D%3D&app_name=5ZOU5ZOp5ZOU5ZOp&req_type=Nw%3D%3D&mini_program_appid=MTEwOTkzNzU1Nw%3D%3D&mini_program_path=cGFnZXMvdmlkZW8vdmlkZW8%2FYnZpZD1CVjF6ZDR5MTE3V0Y%3D&mini_program_type=Mw%3D%3D&cflag=MA%3D%3D&third_sd=dHJ1ZQ%3D%3D' -e pkg_name tv.danmaku.bili";

shell(cmd,true);

waitForActivity("com.tencent.mobileqq.activity.ForwardRecentActivity");

while(!click("搜索"));

setText("卷王培训基地");

while(!click("543780931"));

while(true){
var send =text("发送").findOne(1000);
if (send !=null){send.click();}
// will be null.
var ret=text("返回哔哩哔哩").findOne(1000);

if (ret != null){ret.click();break;}
}

shell("rm /storage/emulated/0/flag")