#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

/*
    What is this?
        Trying to make something faster in C++
        Might go no where, might be something cool.
*/


// Organizaitonal sugar.
class Colors {
    public:
        string green    = "\e[0;32m";
        string yellow   = "\e[0;33m";
        string cyan     = "\e[0;36m";
        string blue     = "\e[1;34m";
        string red      = "\e[1;31m";
        string magenta  = "\e[1;35m";

        string white    = "\e[0m";
};

/*
    Parse and print out the string vector.
    **The string vector**
        Think of it in 2-D, two dimensions to describe piece of data in .csv.
            Sort of 3-D if you view the characters as the third dimension.
    This is orders of magnitude faster than python...
*/

void print_tokens(vector <string> lines) {
    Colors color;
    string colors[] = {color.yellow, color.cyan, color.blue, color.red, color.magenta};

    string attributes [] = {"county: ", "state: ", "ID: ", "cases: ", "deaths: "};

    // I guess this is how you'd parse a csv without a library or something like str.split(',') from python?
    int sep_ct;
    for (int i = 0; i < lines.size(); i++) {
        sep_ct = 0;
        cout << color.green;
        for (int j = 0; j < lines[i].size(); j++) {
            if (lines[i][j] != ',') {
                cout  << lines[i][j];
            }
            else {
                cout << colors[sep_ct] << "\n\t" << attributes[sep_ct];
                sep_ct++;
            }
        }
        cout << endl;
    }
    cout << color.white;
}

void print_file(string fname, string state, string county) {
    string line;
    ifstream covid_data(fname);
    string query = county + ',' + state;
    vector <string> lines;

    // Gets valid lines from .csv based on state and county function arguments.
    if (covid_data) {
      while (getline (covid_data, line, '\n')) {
          if (query.compare(line.substr(11, query.size())) == 0) {
              lines.push_back(line);
            }
        }
      covid_data.close();
    }
    else {
        cout << "Unable to open file" << endl;
    }

    print_tokens(lines);
}

int main(int argc, char** argv) {
    if (argc > 2) {
        string fname;
        string state;
        string county;

        // Will seg fault if argv[i+1] DNE, doesn't matter right now though.
        for (int i = 0; i < argc; i++) {
            string string_arg = argv[i];
            if (string_arg.compare("-f") == 0) {
                fname += argv[i+1];
            }
            else if (string_arg.compare("-s") == 0) {
                state += argv[i+1];
            }
            else if (string_arg.compare("-c") == 0) {
                county += argv[i+1];
            }
        }
        print_file(fname, state, county);
        cout << "File: " << fname << endl;
        return 0;

    }
    else {
        cout << "Error: enter a file with the -f argument.";
        return 1;
    }
}
