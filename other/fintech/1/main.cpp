#include <iostream>
#include <vector>

using namespace std;

const int max_n = 5 * 1e5 + 10;
int tree[4 * max_n];

void build_tree(const vector<int> &a, int v, int tl, int tr) {
    if (tl == tr) {
        tree[v] = a[tl];
    } else {
        int tm = (tl + tr) / 2;
        build_tree(a, v * 2, tl, tm);
        build_tree(a, v * 2 + 1, tm + 1, tr);
        tree[v] = max(tree[v * 2], tree[v * 2 + 1]);
    }
}

int left_index_bigger(int v, int tl, int tr, int l, int r, int value) {
    if (l > r)
        return -1;
    if (l == tl && r == tr) {
        if (tree[v] < value) {
            return -1;
        }
        if (tl == tr) {
            return tl;
        }
    }
    int tm = (tl + tr) / 2;
    int left_index = left_index_bigger(v * 2, tl, tm, l, min(r, tm), value);
    if (left_index != -1) {
        return left_index;
    }
    return left_index_bigger(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r, value);
}


int main() {
    int n;
    cin >> n;

    vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }
    build_tree(a, 1, 0, n - 1);

    vector<int> max_count(n + 1); // ответ. Количество людей от человека вправо про правилам задачи
    max_count[n - 1] = 1;
    for (int i = n - 2; i >= 0; --i) {
        int bigger_idx = left_index_bigger(1, 0, n - 1, i + 1, n - 1, a[i]);
        if (bigger_idx == -1) {
            max_count[i] = 1;
        } else {
            max_count[i] = max_count[bigger_idx] + 1;
        }
    }

    for (int i = 0; i < n; ++i) {
        cout << max_count[i] << ' ';
    }

    return 0;
}