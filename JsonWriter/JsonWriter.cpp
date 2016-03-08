// JsonWriter.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <fstream>
using namespace std;


int main()
{
	ofstream myfile;
	string elements;
	elements = "PLC.json";
	myfile.open(elements);
	myfile << "[\n {\n  ";
	myfile << "\"border\": \"solid\"";
	myfile << "\n }\n]";
	myfile.close();


    return 0;
}

