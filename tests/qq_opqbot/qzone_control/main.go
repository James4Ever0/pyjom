package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
    opqBot := OPQBot.NewBotManager(,"http://192.168.2.2:8899") //前面是机器人的QQ号,后面参数是机器人接口的地址
    err := opqBot.Start()
    if err != nil {
        log.Println(err.Error())
    }
    defer opqBot.Stop()
    opqBot.Wait()
}