/* 
* @Author: zibin 
* @Last Modified time: 2022-05-10 19:45:44  
* @Contact: zibingo@qq.com 
*/
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
#include <algorithm>
#include <math.h>
#include <map>
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
        vector<int>(v).swap(v);
    }
    int n = sqrt(Q.size());
    logger.INFO("成功加载矩阵文件,矩阵:" + to_string(n) + " x " + to_string(n));
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
        vector<int>(a).swap(b);
        vector<int>(b).swap(b);
        vector<int>(c).swap(c);
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
    int f1, f2, f3, paretorank;
    double F, nnd;
    Individual()
    {
        f1 = 0;
        f2 = 0;
        f3 = 0;
        nnd = 0.0;
        paretorank = 0;
    }
    Individual(vector<int> x, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3)
    {
        f1 = 0;
        f2 = 0;
        f3 = 0;
        X = x;
        nnd = 0.0;
        Matrix_X(X, q1, q2, q3, f1, f2, f3);
        f.push_back(f1);
        f.push_back(f2);
        f.push_back(f3);
    }
    ~Individual()
    {
        vector<int>().swap(X);
        vector<int>().swap(f);
    }
};

void Init(int N, vector<Individual> &P, int n, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3, Logger &logger)
{
    for (int i = 0; i < N; i++)
    {
        vector<int> X;
        Create_Decision_Vector(n, X);
        P.push_back(Individual(X, q1, q2, q3));
    }
    logger.INFO("成功初始化种群");
}

vector<Individual> Fast_NonDominate_Sort(int N, vector<Individual> P, map<int, vector<int> > &F)
{
    map<int, int> Pn;
    map<int, vector<int> > Ps;
    vector<int> V;
    int pareto_rank = 1;
    F.insert(pair<int, vector<int> >(pareto_rank, V));
    for (int i = 0; i < N; i++)
    {
        vector<int> v;
        Pn.insert(pair<int, int>(i, 0));
        Ps.insert(pair<int, vector<int> >(i, v));
        for (int j = 0; j < N; j++)
        {
            int l, e, h;
            l = 0;
            e = 0;
            h = 0;
            for (int k = 0; k < 3; k++)
            {
                if (P.at(i).f.at(k) < P.at(j).f.at(k))
                    h += 1;
                else if (P.at(i).f.at(k) == P.at(j).f.at(k))
                    e += 1;
                else
                    l += 1;
            }
            if (h == 0 && e != 3)
                Ps.at(i).push_back(j);
            else if (l == 0 && e != 3)
            {
                map<int, int>::iterator pos = Pn.find(i);
                pos->second += 1;
            }
        }
        map<int, int>::iterator pos = Pn.find(i);
        if (pos->second == 0)
        {
            P.at(i).paretorank = 1;
            F.at(pareto_rank).push_back(i);
        }
    }
    // for (map<int, int>::iterator it = Pn.begin(); it != Pn.end(); it++)
    // {
    //     cout << it->first << " : " << it->second << endl;
    // }
    // cout << endl;
    while (F.at(pareto_rank).size() != 0)
    {
        vector<int> temp;
        for (int i = 0; i < F.at(pareto_rank).size(); i++)
        {
            if (Ps.at(F.at(pareto_rank).at(i)).size() != 0)
            {
                for (int j = 0; j < Ps.at(F.at(pareto_rank).at(i)).size(); j++)
                {
                    Pn.at(Ps.at(F.at(pareto_rank).at(i)).at(j)) -= 1;
                    if (Pn.at(Ps.at(F.at(pareto_rank).at(i)).at(j)) == 0)
                    {
                        P.at(Ps.at(F.at(pareto_rank).at(i)).at(j)).paretorank = pareto_rank + 1;
                        temp.push_back(Ps.at(F.at(pareto_rank).at(i)).at(j));
                    }
                }
            }
        }
        pareto_rank += 1;
        F.insert(pair<int, vector<int> >(pareto_rank, temp));
    }
    map<int, int>().swap(Pn);
    map<int, vector<int> >().swap(Ps);
    return P;
}

bool ParetoRank_Sort(Individual p1, Individual p2)
{
    //根据paretorank大小排序
    return p1.paretorank < p2.paretorank;
}

bool Nnd_Sort(Individual p1, Individual p2)
{
    return p1.nnd > p2.nnd;
}

bool Sort_f1(Individual p1, Individual p2)
{
    return p1.f1 < p2.f1;
}

bool Sort_f2(Individual p1, Individual p2)
{
    return p1.f2 < p2.f2;
}

bool VectorEqual(vector<int> v1, vector<int> v2)
{
    bool flag = true;
    for (int i = 0; i < v1.size(); i++)
    {
        if (v1.at(i) != v2.at(i))
        {
            flag = false;
            break;
        }
    }
    return flag;
}

bool Equal(Individual p1, Individual p2)
{
    bool flag = false;
    if (p1.f1 == p2.f1 && p1.f2 == p2.f2 && p1.f3 == p2.f3 && p1.nnd == p2.nnd && p1.paretorank == p2.paretorank && VectorEqual(p1.X, p2.X))
    {
        flag = true;
    }
    return flag;
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

vector<Individual> Crowding_Distance_Sort(map<int, vector<int> > F1, vector<Individual> P)
{
    vector<Individual> ppp;
    vector<Individual> temp = P;
    sort(temp.begin(), temp.end(), ParetoRank_Sort);
    vector<int> index1;

    for (int i = 0; i < temp.size(); i++)
    {
        for (int j = 0; j < P.size(); j++)
        {
            if (Equal(temp.at(i), P.at(j)))
            {
                index1.push_back(j);
                break;
            }
        }
    }
    // for_each(index1.begin(), index1.end(), print01);
    int current_index = 0;
    for (int pareto_rank = 0; pareto_rank < F1.size() - 1; pareto_rank++)
    {
        vector<Individual> y;
        vector<vector<double> > yF;
        for (int q = 0; q < F1.at(pareto_rank + 1).size(); q++)
        {
            vector<double> v;
            v.push_back(0);
            v.push_back(0);
            v.push_back(0);
            yF.push_back(v);
        }
        int i = 0;
        for (; i < F1.at(pareto_rank + 1).size(); i++)
        {
            y.push_back(temp.at(current_index + i));
        }
        current_index += i;
        for (int i = 0; i < 3; i++)
        {
            vector<int> index_object;
            vector<Individual> objective_sort = y;
            if (i == 0)
                sort(objective_sort.begin(), objective_sort.end(), Sort_f1);
            else
                sort(objective_sort.begin(), objective_sort.end(), Sort_f2);

            for (int j = 0; j < objective_sort.size(); j++)
            {
                for (int k = 0; k < y.size(); k++)
                {
                    if (Equal(objective_sort.at(j), y.at(k)))
                    {
                        index_object.push_back(k);
                        break;
                    }
                }
            }

            int fmin = objective_sort.at(0).f.at(i);
            int fmax = objective_sort.at(objective_sort.size() - 1).f.at(i);
            yF.at(index_object.at(0)).at(i) = __DBL_MAX__;
            yF.at(index_object.at(index_object.size() - 1)).at(i) = __DBL_MAX__;
            for (int j = 1; j < index_object.size() - 1; j++)
            {
                int pre_f = objective_sort.at(j - 1).f.at(i);
                int next_f = objective_sort.at(j + 1).f.at(i);
                if (fmax - fmin == 0)
                {
                    yF.at(index_object.at(j)).at(i) = __DBL_MAX__;
                }
                else
                {
                    yF.at(index_object.at(j)).at(i) = double(next_f - pre_f) / (fmax - fmin);
                }
            }
        }
        vector<double> nd;
        for (int b = 0; b < yF.size(); b++)
        {
            nd.push_back(yF.at(b).at(0) + yF.at(b).at(1));
        }
        for (int c = 0; c < y.size(); c++)
        {
            y.at(c).nnd = nd.at(c);
            ppp.push_back(y.at(c));
        }
    }
    vector<Individual>().swap(temp);
    return ppp;
}

Individual Cross_Mutation(Individual p1, Individual p2, float Pc, float Pm, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3)
{
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
    return Individual(X, q1, q2, q3);
}

vector<Individual> Elitism(int N, vector<Individual> combine_chromo2)
{
    vector<Individual> chromo, chromo_rank;
    int index1 = 0;
    int index2 = 0;
    chromo_rank = combine_chromo2;
    sort(chromo_rank.begin(), chromo_rank.end(), ParetoRank_Sort);
    int flag = chromo_rank.at(N - 1).paretorank;
    for (int i = 0; i < chromo_rank.size(); i++)
    {
        if (chromo_rank.at(i).paretorank == flag)
        {
            index1 = i;
            break;
        }
        else
            chromo.push_back(chromo_rank.at(i));
    }
    for (int i = 0; i < chromo_rank.size(); i++)
    {
        if (chromo_rank.at(i).paretorank == (flag + 1))
        {
            index2 = i;
            break;
        }
    }
    vector<Individual> temp, temp_crowd;
    int aaa = index1;
    if (index2 == 0)
        index2 = chromo_rank.size();
    while (aaa < index2)
    {
        temp.push_back(chromo_rank.at(aaa));
        aaa++;
    }
    temp_crowd = temp;
    sort(temp_crowd.begin(), temp_crowd.end(), Nnd_Sort);
    int remainN = N - index1;
    for (int i = 0; i < remainN; i++)
    {
        chromo.push_back(temp_crowd.at(i));
    }
    return chromo;
}

int Dominate(vector<int> f1, vector<int> f2)
{
    int res;
    int low, equal, high = 0;
    int m = f1.size();
    for (int i = 0; i < m; i++)
    {
        if (f1.at(i) < f2.at(i))
            high += 1;
        else if (f1.at(i) == f2.at(i))
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

Individual LocalSearch(Individual parent, int MaxDepth, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3)
{
    int depth = 0;
    vector<int> temp = parent.X;
    vector<int> bestX = parent.X;
    vector<int> f = parent.f;
    vector<int> DeltaC1, DeltaC2, DeltaC3;
    InitDeltaC(parent.X, q1, q2, q3, DeltaC1, DeltaC2, DeltaC3);
    while (depth < MaxDepth)
    {
        int flipindex = 0;
        while (flipindex < temp.size())
        {
            //使用公式求得翻转前后差值
            vector<int> off_f;
            int f1 = f.at(0) + DeltaC1[flipindex];
            int f2 = f.at(1) + DeltaC2[flipindex];
            int f3 = f.at(2) + DeltaC3[flipindex];
            off_f.push_back(f1);
            off_f.push_back(f2);
            off_f.push_back(f3);
            if (Dominate(off_f, f) == 1)
            {
                f = off_f;
                temp.at(flipindex) = 1 - temp.at(flipindex);
                bestX = temp;
                UpdateDeltaC(temp, flipindex, q1, q2, q3, DeltaC1, DeltaC2, DeltaC3);
                break;
            }
            flipindex++;
        }
        depth++;
    }
    return Individual(bestX, q1, q2, q3);
}
Individual TabuSearch(Individual parent, int MaxDepth, int Length, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3)
{
    int n = parent.X.size();
    vector<int> TaboList, DeltaC1, DeltaC2, DeltaC3;
    InitTaboList(TaboList, n);
    InitDeltaC(parent.X, q1, q2, q3, DeltaC1, DeltaC2, DeltaC3);
    vector<int> bestX = parent.X;
    vector<int> bestf = parent.f;
    vector<int> curX = parent.X;
    vector<int> curf = parent.f;
    int depth = 1;
    while (depth <= MaxDepth)
    {
        int flipindex = n;
        vector<int> tempf = curf;
        double distance = __DBL_MAX__;
        for (int i = 0; i < n; i++)
        {
            vector<int> off_f;
            int off_f1 = curf.at(0) + DeltaC1.at(i);
            int off_f2 = curf.at(1) + DeltaC2.at(i);
            int off_f3 = curf.at(2) + DeltaC3.at(i);
            off_f.push_back(off_f1);
            off_f.push_back(off_f2);
            off_f.push_back(off_f3);
            if (JudgeTaboo(TaboList, i) == false)
            {
                if (Dominate(off_f, tempf) == 1)
                {
                    flipindex = i;
                    tempf = off_f;
                }
                else if (Dominate(off_f, tempf) == -1 && sqrt(pow(off_f1 - tempf.at(0), 2) + pow(off_f2 - tempf.at(1), 2) + pow(off_f3 - tempf.at(2), 2)) < distance)
                {
                    distance = sqrt(pow(off_f1 - tempf.at(0), 2) + pow(off_f2 - tempf.at(1), 2) + pow(off_f3 - tempf.at(2), 2));
                    flipindex = i;
                }
            }
            else
            {
                if (Dominate(off_f, bestf) == 1)
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
        curX.at(flipindex) = 1 - curX.at(flipindex);
        UpdateTaboList(TaboList);
        JoinTaboList(TaboList, flipindex, Length);
        UpdateDeltaC(curX, flipindex, q1, q2, q3, DeltaC1, DeltaC2, DeltaC3);
        if (Dominate(curf, bestf) == 1)
        {
            bestf = curf;
            bestX = curX;
        }
        depth++;
    }
    return Individual(bestX, q1, q2, q3);
}

void Evolution(int Max_Gen, int SearchMethod, int SearchDepth, int N, vector<Individual> &P, map<int, vector<int> > F1, float Pc, float Pm, vector<vector<int> > q1, vector<vector<int> > q2, vector<vector<int> > q3, time_t t, Logger &logger)
{
    int gen = 1;
    while (gen <= Max_Gen)
    {
        vector<Individual> offspring;
        for (int i = 0; i < N; i++)
        {
            Individual p1 = P.at(rand() % P.size());
            Individual p2 = P.at(rand() % P.size());
            Individual p = Cross_Mutation(p1, p2, Pc, Pm, q1, q2, q3);
            if (SearchMethod == 0)
                offspring.push_back(p);
            else if (SearchMethod == 1)
                offspring.push_back(LocalSearch(p, SearchDepth, q1, q2, q3));
            else
                offspring.push_back(TabuSearch(p, SearchDepth, SearchDepth / 5, q1, q2, q3));
        }
        vector<Individual> combine_P = offspring;
        //合并子代父代
        for (int i = 0; i < P.size(); i++)
        {
            combine_P.push_back(P.at(i));
        }
        map<int, vector<int> > F2;
        vector<Individual> combine_P1 = Fast_NonDominate_Sort(combine_P.size(), combine_P, F2);
        vector<Individual> combine_P2 = Crowding_Distance_Sort(F2, combine_P1);
        P = Elitism(N, combine_P2);
        logger.INFO("已进化:" + to_string(gen) + "代," + "已耗时:" + to_string((double)(clock() - t) / CLOCKS_PER_SEC) + "秒");
        gen++;
    }
}
int main(int argc, char *argv[])
{
    try
    {
        /*---------------------------------------------------*/
        string occ = argv[1];
        int n = stoi(argv[2]);
        string Pm1 = argv[3];
        //这样转pm浮点数精确度跟输入一致
        float Pm = atof(Pm1.c_str());
        int Max_Gen = stoi(argv[4]);
        int SearchMethod = stoi(argv[5]);
        int Run_Num = stoi(argv[6]);
        string CppLogName = argv[7];
        string EpName = argv[8];
        float Pc = 1.0;
        int N = 100;
        int m = 3;
        /*---------------------------------------------------*/
        int SearchDepth = 10;
        /*---------------------------------------------------*/

        srand(time(NULL)); //设置随机数种子，使每次产生的随机序列不同
        clock_t start, finish;
        start = clock();
        Logger logger(Logger::file_and_terminal, Logger::info, CppLogName);
        string QName = "../../instances/mubqp_" + occ + "_3_" + to_string(n) + "_0.8_0.dat";
        start = clock();
        vector<vector<int> > Q, q1, q2, q3;
        map<int, vector<int> > F1;
        vector<Individual> P, P1;
        Read_Matrix_file(QName, Q, logger);
        Return_Matrix(Q, q1, q2, q3);
        Init(N, P, n, q1, q2, q3, logger);
        Fast_NonDominate_Sort(N, P, F1);
        P = Crowding_Distance_Sort(F1, P);
        Evolution(Max_Gen, SearchMethod, SearchDepth, N, P, F1, Pc, Pm, q1, q2, q3, start, logger);
        Write_EP_File(P, EpName);
        finish = clock();
        logger.INFO("总耗时:" + to_string((double)(finish - start) / CLOCKS_PER_SEC) + "秒");
    }
    catch (const char *msg)
    {
        cerr << msg << endl;
    }
}