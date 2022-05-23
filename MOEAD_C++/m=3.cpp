/* 
* @Author: zibin 
* @Last Modified time: 2022-05-10 19:43:15  
* @Contact: zibingo@qq.com 
*/
include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
#include <algorithm>
#include <math.h>
#include "time.h"
#include "Logger.h"
using namespace std;

void Read_Matrix_file(string path, vector<vector<int> > &Q, Logger &logger)
{
    ifstream f;
    int a, b, c;
    f.open(path, ios::in);
    if (f.fail())
    {
        throw "矩阵文件路径出错!";
    }
    while (!f.eof())
    {
        vector<int> v;
        f >> a >> b >> c;
        v.push_back(a);
        v.push_back(b);
        v.push_back(c);
        Q.push_back(v);
        vector<int>().swap(v);
    }
    int n = sqrt(Q.size());
    logger.INFO("成功加载矩阵文件,矩阵:" + to_string(n) + " x " + to_string(n));
    f.close();
}

void Read_Weight(string path, vector<vector<double> > &Weights, Logger &logger)
{
    ifstream f;
    double a, b, c;
    f.open(path, ios::in);
    if (f.fail())
    {
        throw "权重文件路径错误!";
    }
    while (!f.eof())
    {
        vector<double> v;
        f >> a >> b >> c;
        v.push_back(a);
        v.push_back(b);
        v.push_back(c);
        Weights.push_back(v);
        vector<double>().swap(v);
    }
    if (Weights.size() == 102)
    {
        Weights.pop_back();
    }
    logger.INFO("成功加载权重文件,大小:" + to_string(Weights.size()));
    f.close();
}

void Return_Matrix(vector<vector<int> > Q, vector<vector<int> > &q1, vector<vector<int> > &q2, vector<vector<int> > &q3)
{
    int n = sqrt(Q.size());
    for (int i = 0; i < n; i++)
    {
        vector<int> a, b, c;
        for (int j = i; j < Q.size(); j += n)
        {
            a.push_back(Q.at(j).at(0));
            b.push_back(Q.at(j).at(1));
            c.push_back(Q.at(j).at(2));
        }
        q1.push_back(a);
        q2.push_back(b);
        q3.push_back(c);
        vector<int>().swap(a);
        vector<int>().swap(b);
        vector<int>().swap(c);
    }
}

void Neighbor(vector<vector<double> > Weights, vector<vector<int> > &B, int T)
{
    int N = Weights.size();
    for (int i = 0; i < N; i++)
    {
        vector<long double> v;
        vector<int> index;
        for (int j = 0; j < N; j++)
        {
            long double d = sqrt(pow(Weights.at(i).at(0) - Weights.at(j).at(0), 2) + pow(Weights.at(i).at(1) - Weights.at(j).at(1), 2) + pow(Weights.at(i).at(2) - Weights.at(j).at(2), 2));
            v.push_back(d);
        }
        //实现python numpy.argsort()功能
        set<long double> s(v.begin(), v.end());
        for (set<long double>::iterator it = s.begin(); it != s.end(); it++)
        {
            for (int i = 0; i < v.size(); i++)
            {
                if (*it == v.at(i))
                {
                    index.push_back(i);
                }
            }
        }
        B.push_back(index);
        vector<long double>().swap(v);
        vector<int>().swap(index);
        set<long double>().swap(s);
    }
}

void Create_Decision_Vector(int n, vector<int> &X)
{
    for (int i = 0; i < n; i++)
    {
        X.push_back(rand() % 2);
    }
}

void Matrix_X(vector<int> X, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3, int &sum1, int &sum2, int &sum3)
{
    int n = X.size();
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            sum1 += q1.at(i).at(j) * X.at(i) * X.at(j);
            sum2 += q2.at(i).at(j) * X.at(i) * X.at(j);
            sum3 += q3.at(i).at(j) * X.at(i) * X.at(j);
        }
    }
}

class Individual
{
public:
    vector<int> X;
    vector<int> f;
    vector<double> W;
    int f1, f2, f3;
    double F;
    Individual()
    {
        F = 0.0;
        f1 = 0;
        f2 = 0;
        f3 = 0;
        //为什么f1,f2数那么大，原来，没有调用默认的构造函数，所以f1,f2没有初始化
        // cout << "默认构造" << endl;
    }
    Individual(vector<int> x, vector<double> w, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3)
    {
        // cout << "自定义构造" << endl;
        f1 = 0;
        f2 = 0;
        f3 = 0;
        X = x;
        W = w;
        Matrix_X(X, q1, q2, q3, f1, f2, f3);
        f.push_back(f1);
        f.push_back(f2);
        f.push_back(f3);
        F = W.at(0) * f1 + W.at(1) * f2 + W.at(2) * f3;
    }
    ~Individual()
    {
        vector<int>().swap(X);
        vector<int>().swap(f);
        vector<double>().swap(W);
    }
};

void Init(int N, vector<Individual> &P, vector<vector<double> > Weights, int n, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3, Logger &logger)
{
    for (int i = 0; i < N; i++)
    {
        vector<int> X;
        Create_Decision_Vector(n, X);
        P.push_back(Individual(X, Weights.at(i), q1, q2, q3));
    }
    logger.INFO("成功初始化种群");
}

Individual cross_mutation(Individual p1, Individual p2, vector<double> W, float Pc, float Pm, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3)
{
    //--------------一个后代--------------
    int n = p1.X.size();
    vector<int> X;
    if ((double(rand() % 99) / 100.0) < Pc)
    {
        vector<int> model;
        Create_Decision_Vector(n, model);
        for (int i = 0; i < n; i++)
        {
            if (model.at(i) == 0)
            {
                X.push_back(p1.X.at(i));
            }
            else
            {
                X.push_back(p2.X.at(i));
            }
        }
    }
    for (int j = 0; j < n; j++)
    {
        if ((double(rand() % 99) / 100.0) < Pm)
        {
            X.at(j) = 1 - X.at(j);
        }
    }
    return Individual(X, W, q1, q2, q3);
}

int Dominate(Individual p1, Individual p2)
{
    int res;
    int low, equal, high = 0;
    int m = p1.f.size();
    for (int i = 0; i < m; i++)
    {
        if (p1.f.at(i) < p2.f.at(i))
            high += 1;
        else if (p1.f.at(i) == p2.f.at(i))
            equal += 1;
        else
            low += 1;
    }
    if (high == 0 && equal != m)
        res = 1;
    else if (low == 0 && equal != m)
        res = 0;
    else if (equal == m)
        res = -2;
    else
        res = -1;
    return res;
}

void UpdateEp(Individual p, vector<Individual> &EP)
{
    bool flag = true;
    for (int k = 0; k < EP.size(); k++)
    {
        int res = Dominate(p, EP.at(k));
        if (res == 1 || res == -2)
        {
            EP.erase(EP.begin() + k);
        }
        if (res == 0)
        {
            flag = false;
        }
    }
    if (flag == true)
    {
        EP.push_back(p);
    }
}

void UpdateDomain(Individual p, int i, int T, vector<Individual> &P, vector<vector<int> > B)
{
    for (int j = 0; j < T; j++)
    {
        double F = P.at(B.at(i).at(j)).W.at(0) * p.f1 + P.at(B.at(i).at(j)).W.at(1) * p.f2 + +P.at(B.at(i).at(j)).W.at(2) * p.f3;
        if (F > P.at(B.at(i).at(j)).F)
        {
            P.at(B.at(i).at(j)).F = F;
            P.at(B.at(i).at(j)).X = p.X;
        }
    }
}

void Write_EP_File(vector<Individual> EP, string FileName)
{
    ofstream f;
    f.open(FileName, ios::out);
    for (int i = 0; i < EP.size(); i++)
    {
        f << EP.at(i).f1 << " " << EP.at(i).f2 << " " << EP.at(i).f3 << endl;
    }
    f.close();
}

void InitTaboList(vector<int> &TaboList, int n)
{
    for (int i = 0; i < n; i++)
        TaboList.push_back(0);
}

int Formula(int FlipIndex, vector<int> X, vector<vector<int> > q)
{
    int sum = 0;
    int n = X.size();
    for (int j = 0; j < n; j++)
    {
        if (j != FlipIndex)
            sum += (q.at(FlipIndex).at(j) + q.at(j).at(FlipIndex)) * X.at(j);
    }
    return (1 - 2 * X.at(FlipIndex)) * (sum + q.at(FlipIndex).at(FlipIndex));
}

void InitDeltaC(vector<int> X, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3, vector<int> &DeltaC1, vector<int> &DeltaC2, vector<int> &DeltaC3)
{
    int n = X.size();
    for (int j = 0; j < n; j++)
    {
        DeltaC1.push_back(Formula(j, X, q1));
        DeltaC2.push_back(Formula(j, X, q2));
        DeltaC3.push_back(Formula(j, X, q3));
    }
}

bool JudgeTaboo(vector<int> TaboList, int i)
{
    bool res;
    if (TaboList.at(i) == 0)
        res = false;
    else
        res = true;
    return res;
}

void JoinTaboList(vector<int> &TaboList, int r, int Length)
{
    TaboList.at(r) = Length;
}
void UpdateTaboList(vector<int> &TaboList)
{
    for (int i = 0; i < TaboList.size(); i++)
    {
        if (TaboList.at(i) != 0)
            TaboList.at(i)--;
    }
}

void UpdateDeltaC(vector<int> X, int j, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3, vector<int> &DeltaC1, vector<int> &DeltaC2, vector<int> &DeltaC3)
{
    int n = X.size();
    for (int i = 0; i < n; i++)
    {
        if (i == j)
        {
            DeltaC1.at(i) = -DeltaC1.at(i);
            DeltaC2.at(i) = -DeltaC2.at(i);
            DeltaC3.at(i) = -DeltaC3.at(i);
        }
        else
        {
            DeltaC1.at(i) -= (q1.at(i).at(j) + q1.at(j).at(i)) * (1 - 2 * X.at(i)) * (1 - 2 * X.at(j));
            DeltaC2.at(i) -= (q2.at(i).at(j) + q2.at(j).at(i)) * (1 - 2 * X.at(i)) * (1 - 2 * X.at(j));
            DeltaC3.at(i) -= (q3.at(i).at(j) + q3.at(j).at(i)) * (1 - 2 * X.at(i)) * (1 - 2 * X.at(j));
        }
    }
}

Individual TabuSearch(Individual parent, int MaxDepth, int Length, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3)
{
    int n = parent.X.size();
    vector<int> TaboList, DeltaC1, DeltaC2, DeltaC3;
    InitTaboList(TaboList, n);
    InitDeltaC(parent.X, q1, q2, q3, DeltaC1, DeltaC2, DeltaC3);

    double bestF = parent.F;
    vector<int> bestX = parent.X;
    vector<int> curX = parent.X;
    vector<int> curf = parent.f;
    double curF = parent.F;
    int depth = 1;
    while (depth <= MaxDepth)
    {
        int flipindex = n;
        double DeltaC = __DBL_MAX__ * -1;
        for (int i = 0; i < n; i++)
        {
            int off_f1 = curf.at(0) + DeltaC1.at(i);
            int off_f2 = curf.at(1) + DeltaC2.at(i);
            int off_f3 = curf.at(2) + DeltaC3.at(i);
            double offF = off_f1 * parent.W.at(0) + off_f2 * parent.W.at(1) + off_f3 * parent.W.at(2);
            if (JudgeTaboo(TaboList, i) == false)
            {
                if (offF > DeltaC)
                {
                    flipindex = i;
                    DeltaC = offF;
                }
            }
            else
            {
                if (offF > bestF)
                {
                    flipindex = i;
                    break;
                }
            }
        }
        int off_f1 = curf.at(0) + DeltaC1.at(flipindex);
        int off_f2 = curf.at(1) + DeltaC2.at(flipindex);
        int off_f3 = curf.at(2) + DeltaC3.at(flipindex);
        curf.at(0) = off_f1;
        curf.at(1) = off_f2;
        curf.at(2) = off_f3;
        double offF = off_f1 * parent.W.at(0) + off_f2 * parent.W.at(1) + off_f3 * parent.W.at(2);
        curX.at(flipindex) = 1 - curX.at(flipindex);
        UpdateTaboList(TaboList);
        JoinTaboList(TaboList, flipindex, Length);
        UpdateDeltaC(curX, flipindex, q1, q2, q3, DeltaC1, DeltaC2, DeltaC3);
        if (offF > bestF)
        {
            bestF = offF;
            bestX = curX;
        }
        depth++;
    }
    return Individual(bestX, parent.W, q1, q2, q3);
}

Individual LocalSearch(Individual parent, int MaxDepth, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3)
{
    int depth = 0;
    vector<int> temp = parent.X;
    vector<int> bestX = parent.X;
    vector<int> f = parent.f;
    double F = parent.F;
    vector<int> DeltaC1, DeltaC2, DeltaC3;
    InitDeltaC(parent.X, q1, q2, q3, DeltaC1, DeltaC2, DeltaC3);
    while (depth < MaxDepth)
    {
        int flipindex = 0;
        while (flipindex < temp.size())
        {
            //使用公式求得翻转前后差值
            int f1 = f.at(0) + DeltaC1[flipindex];
            int f2 = f.at(1) + DeltaC2[flipindex];
            int f3 = f.at(2) + DeltaC3[flipindex];
            double offF = f1 * parent.W.at(0) + f2 * parent.W.at(1) + f3 * parent.W.at(2);
            if (offF > F)
            {
                F = offF;
                f.at(0) = f1;
                f.at(1) = f2;
                f.at(2) = f3;
                temp.at(flipindex) = 1 - temp.at(flipindex);
                bestX = temp;
                UpdateDeltaC(temp, flipindex, q1, q2, q3, DeltaC1, DeltaC2, DeltaC3);
                break;
            }
            flipindex++;
        }
        depth++;
    }
    return Individual(bestX, parent.W, q1, q2, q3);
}

void Evolution(int Max_Gen, int SearchMethod, int SearchDepth, vector<Individual> &P, vector<vector<int> > B, int N, int T, float Pc, float Pm, vector<Individual> &EP, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3, int t, Logger &logger)
{
    int gen = 1;
    while (gen <= Max_Gen)
    {
        for (int i = 0; i < N; i++)
        {
            int k = (rand() % (T));
            int l = (rand() % (T));
            /* ------------------ 一个后代 ------------------*/
            Individual p, p1;
            p = cross_mutation(P.at(B.at(i).at(k)), P.at(B.at(i).at(l)), P.at(i).W, Pc, Pm, q1, q2, q3);
            if (SearchMethod == 0)
            {
                UpdateEp(p, EP);
                UpdateDomain(p, i, T, P, B);
            }
            else if (SearchMethod == 1)
            {
                p1 = LocalSearch(p, SearchDepth, q1, q2, q3);
                UpdateEp(p1, EP);
                UpdateDomain(p1, i, T, P, B);
            }
            else
            {
                p1 = TabuSearch(p, SearchDepth, SearchDepth / 2, q1, q2, q3);
                UpdateEp(p1, EP);
                UpdateDomain(p1, i, T, P, B);
            }
        }
        /*----------------------------------------------------*/
        logger.INFO("已进化:" + to_string(gen) + "代," + "已耗时:" + to_string((double)(clock() - t) / CLOCKS_PER_SEC) + "秒");
        if (gen == Max_Gen)
        {
            logger.INFO("EP数量:" + to_string(EP.size()));
        }
        gen++;
    }
}

int main(int argc, char *argv[])
{
    try
    {
        /*---------------------------------------------------*/
        string occ = argv[1];                  //相关系数
        int n = stoi(argv[2]);                 //决策向量个数
        string Pm1 = argv[3];                  //变异概率
        //这样转pm浮点数精确度跟输入一致    
        float Pm = atof(Pm1.c_str());           
        int Max_Gen = stoi(argv[4]);           //最大进化代数
        int SearchMethod = stoi(argv[5]);      //0:不使用搜索方法 1:使用局部搜索 2:使用禁忌搜索
        int Run_Num = stoi(argv[6]);           //当前运行次数
        string CppLogName = argv[7];           //生成日志文件名字
        string EpName = argv[8];               //生成EP文件名字
        /*---------------------------------------------------*/
        float Pc = 1.0;                        //交叉概率
        int T = 5;                             //邻居个数
        int m = 2;                             //目标数量
        int SearchDepth = 10;                  //搜索深度
        /*---------------------------------------------------*/
        srand(time(NULL)); //设置随机数种子，使每次产生的随机序列不同
        clock_t start, finish;
        start = clock();
        Logger logger(Logger::file_and_terminal, Logger::info, CppLogName);
        string QName = "../instances/mubqp_" + occ + "_3_" + to_string(n) + "_0.8_0.dat";
        string WName = "../instances/weight_m=3.txt";
        vector<vector<int> > Q, q1, q2, q3, B;
        vector<vector<double> > Weights;
        vector<Individual> P, EP;
        Q.reserve(pow(n, 2));
        Read_Matrix_file(QName, Q, logger);
        Read_Weight(WName, Weights, logger);
        Return_Matrix(Q, q1, q2, q3);
        int N = Weights.size();
        Neighbor(Weights, B, T);
        Init(N, P, Weights, n, q1, q2, q3, logger);
        Evolution(Max_Gen, SearchMethod, SearchDepth, P, B, N, T, Pc, Pm, EP, q1, q2, q3, start, logger);
        Write_EP_File(EP, EpName);
        finish = clock();
        logger.INFO("总耗时:" + to_string((double)(finish - start) / CLOCKS_PER_SEC) + "秒");
    }
    catch (const char *msg)
    {
        cerr << msg << endl;
    }
}