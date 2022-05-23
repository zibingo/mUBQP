#ifndef LOG_SYS_H
#define LOG_SYS_H
#include <iostream>
#include <fstream>
#include <string>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
using std::cout;
using std::endl;
using std::ios;
using std::string;
using std::to_string;

string currTime()
{
    // 获取当前时间，并规范表示
    char tmp[64];
    time_t ptime;
    time(&ptime); // time_t time (time_t* timer);
    strftime(tmp, sizeof(tmp), "%Y-%m-%d %H:%M:%S", localtime(&ptime));
    return tmp;
}

class Logger
{
public:
    enum log_level
    {
        debug,
        info,
        warning,
        error
    }; // 日志等级
    enum log_target
    {
        file,
        terminal,
        file_and_terminal
    }; // 日志输出目标
private:
    std::ofstream outfile;                         // 将日志输出到文件的流对象
    log_target target;                             // 日志输出目标
    string path;                                   // 日志文件路径
    log_level level;                               // 日志等级
    void output(string text, log_level act_level); // 输出行为
public:
    Logger(); // 默认构造函数
    Logger(log_target target, log_level level, string path);
    void DEBUG(string text);
    void INFO(string text);
    void WARNING(string text);
    void ERROR(string text);
};
Logger::Logger()
{
    // 默认构造函数
    this->target = terminal;
    this->level = debug;
}

Logger::Logger(log_target target, log_level level, string path)
{
    this->target = target;
    this->path = path;
    this->level = level;
    string tmp = ""; // 双引号下的常量不能直接相加，所以用一个string类型做转换
    // string welcome_dialog = tmp + "[Welcome] " + __FILE__ + " " + currTime() + " : " + "=== Start logging ===\n";
    if (target != terminal)
    {
        this->outfile.open(path, ios::out | ios::app); // 打开输出文件
        // this->outfile << welcome_dialog;
    }
    // if (target != file)
    // {
    //     // 如果日志对象不是仅文件
    //     cout << welcome_dialog;
    // }
}

void Logger::output(string text, log_level act_level)
{
    string prefix;
    if (act_level == debug)
        prefix = "[DEBUG]   ";
    else if (act_level == info)
        prefix = "[INFO]    ";
    else if (act_level == warning)
        prefix = "[WARNING] ";
    else if (act_level == error)
        prefix = "[ERROR]   ";
    else
        prefix = "";
    prefix += " ";
    string output_content = currTime() + " " + prefix + " : " + text + "\n";
    if (this->level <= act_level && this->target != file)
    {
        // 当前等级设定的等级才会显示在终端，且不能是只文件模式
        cout << output_content;
    }
    if (this->target != terminal)
        outfile << output_content;
}

void Logger::DEBUG(string text)
{
    this->output(text, debug);
}

void Logger::INFO(string text)
{
    this->output(text, info);
}

void Logger::WARNING(string text)
{
    this->output(text, warning);
}

void Logger::ERROR(string text)
{
    this->output(text, error);
}
void logger_test()
{
    Logger logger(Logger::file_and_terminal, Logger::debug, "result.log");
    logger.DEBUG("What happend?");
    logger.INFO("This is good.");
    logger.WARNING("Yes...");
    logger.ERROR("IO Error!");
}

#endif
