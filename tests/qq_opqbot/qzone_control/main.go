package main

import "fmt"
import "github.com/mcoo/OPQBot"
func main() {
    fmt.Println("Hello, World!")
    qqNumber int64 :=917521610
    serverPort:="8784"
    opqBot := OPQBot.NewBotManager(qqNumber,"http://localhost:"+serverPort) //前面是机器人的QQ号,后面参数是机器人接口的地址
    err := opqBot.Start()
    if err != nil {
        log.Println(err.Error())
    }
    defer opqBot.Stop()
    opqBot.Wait()
}