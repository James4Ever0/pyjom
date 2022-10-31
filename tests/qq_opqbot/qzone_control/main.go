package main

import (
	"fmt"
	"github.com/mcoo/OPQBot"
	"github.com/mcoo/OPQBot/qzone"
)

func main() {
	fmt.Println("Hello, World!")
	qqNumber := int64(917521610)
	serverPort := "8784"
	opqBot := OPQBot.NewBotManager(qqNumber, "http://localhost:"+serverPort) //前面是机器人的QQ号,后面参数是机器人接口的地址
	err := opqBot.Start()
	if err != nil {
		fmt.Println(err.Error())
	}
	defer opqBot.Stop() // what is this defer?
	// fmt.Println("waiting!")
    ck, _ := opqBot.GetUserCookie()
	qz := qzone.NewQzoneManager(opqBot.QQ, ck)
    fmt.Println(qz)
	// opqBot.Wait() // wait for what? what are you doing?
	// fmt.Println("logic follows here?") // nothing here!
}
