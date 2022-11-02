pkg="com.tencent.weishi"
act="com.tencent.oscar.module.discovery.ui.GlobalSearchActivity"

app.startActivity({root:true,
packageName:pkg,className:act,
action:"View"})

waitForActivity(act)

setText("猫猫")

KeyCode("KEYCODE_ENTER")
