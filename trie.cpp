//#include <gmp.h>
#include "trie.hpp"

#include <iostream>
#include <utility>
#include <algorithm>
#include <cassert>



trie::trie() {}

trie_node* copy_constructor_recur(const trie_node* original)
{
    trie_node* new_node = new trie_node;
    if (original != nullptr)
    {
        new_node->payload = original->payload;
        new_node->is_terminal = original->is_terminal;
        new_node->parent = original->parent;
        for (int i = 0; i < num_chars; ++i)
        {
            if (original->children[i] != nullptr)
            {
                new_node->children[i] = copy_constructor_recur(original->children[i]);
            }
        }
    }
    return new_node;
}

trie::trie(const trie &rhs)
{
    m_size = rhs.m_size;
    m_root = copy_constructor_recur(rhs.m_root);
}

trie& trie::operator=(const trie &rhs)
{
    m_size = rhs.m_size;
    m_root = copy_constructor_recur(rhs.m_root);
    return *this;
}

trie::trie(trie &&rhs) : m_root(rhs.m_root),
                         m_size(rhs.m_size)
{
    rhs.m_root = nullptr;
}

trie& trie::operator=(trie &&rhs)
{
    m_size = rhs.m_size;
    m_root = rhs.m_root;
    rhs.m_root = nullptr;
    return *this;
}


trie::trie(const std::vector<std::string> &strings)
{
    for (auto& string : strings)
    {
        this->insert(string);
    }
}

void delete_recur(trie_node* kornout)
{
//    if (kornout == nullptr) return;

    for (auto node : kornout->children)
    {
        if (node != nullptr)
        {
            delete_recur(node);
//            delete node;
        }
    }
//    kornout->payload = 0;
//    kornout->is_terminal = false;
//    kornout->parent = nullptr;
    delete kornout;
}

trie::~trie()
{
    if (m_root != nullptr)
    {
        delete_recur(m_root);
    }
    m_root = nullptr;
    m_size = 0;
}


bool trie::erase(const std::string &str)
{
    const char* str_ptr = str.c_str();
    trie_node* kornout = m_root;

    if (kornout == nullptr || str.empty())
    {
        return false;
    }


    while (*str_ptr)
    {
        if (kornout->children[*str_ptr] == nullptr)
        {
            return false;
        }
        kornout = kornout->children[*str_ptr];
        str_ptr++;
    }
    if (kornout->is_terminal)
    {
        m_size--;
        kornout->is_terminal = false;
        return true;
    }
    else
    {
        return false;
    }
}

bool trie::insert(const std::string &str)
{
    const char* str_ptr = str.c_str();
    if (m_root == nullptr)
    {
        m_root = new trie_node;
    }
    trie_node* kornout = m_root;

    while (*str_ptr)
    {
        if (kornout->children[*str_ptr] == nullptr)
        {
            trie_node* new_node = new trie_node;
            new_node->parent = kornout;
            new_node->payload = *str_ptr;
//            trie_node* new_node = new trie_node{.parent = kornout, .payload = *str_ptr};
            kornout->children[*str_ptr] = new_node;
        }
        kornout = kornout->children[*str_ptr];
        str_ptr++;
    }
    if (kornout->is_terminal)
    {
        return false;
    }
    else
    {
        kornout->is_terminal = true;
        m_size++;
        return true;
    }
}

bool trie::contains(const std::string &str) const
{
    const char* str_ptr = str.c_str();
    trie_node* kornout = m_root;

    if (kornout == nullptr)
    {
        return false;
    }

    while (*str_ptr)
    {
        if (kornout->children[*str_ptr] == nullptr)
        {
            return false;
        }
        kornout = kornout->children[*str_ptr];
        str_ptr++;
    }
    if (kornout->is_terminal)
    {
        return true;
    }
    else
    {
        return false;
    }
}

size_t trie::size() const
{
    std::cout << "trie size: " << m_size << "\n";
    return m_size;
}

bool trie::empty() const
{
    return m_size == 0;
}

std::vector<std::string> trie::search_by_prefix(const std::string &prefix) const
{
    std::vector<std::string> v (1, "") ;
    return v;
}

std::vector<std::string> trie::get_prefixes(const std::string &str) const
{
    std::vector<std::string> v (1, "") ;
    return v;
}

void trie::swap(trie &rhs)
{
    trie_node* my_root = m_root;
    size_t my_size = m_size;
    m_root = rhs.m_root;
    m_size = rhs.m_size;
    rhs.m_root = my_root;
    rhs.m_size = my_size;
}


trie::const_iterator::const_iterator(const trie_node *node)
{
    current_node = node;
}

trie::const_iterator trie::begin() const
{
    return trie::const_iterator();
}

trie::const_iterator trie::end() const
{
    return trie::const_iterator();
}

trie::const_iterator & trie::const_iterator::operator++()
{
    ++current_node;
    return *this;
}

trie::const_iterator trie::const_iterator::operator++(int)
{
    trie::const_iterator copy(*this);
    ++*this;
    return copy;
}

trie::const_iterator::reference trie::const_iterator::operator*() const
{
    return "";
}

bool trie::const_iterator::operator==(const const_iterator &rhs) const
{
    return current_node == rhs.current_node;
}

bool trie::const_iterator::operator!=(const const_iterator &rhs) const
{
    return current_node != rhs.current_node;
}


bool operator_equals_recur(const trie_node* lhs, const trie_node* rhs)
{
//    bool is_equal = true;
    if (lhs->is_terminal == rhs->is_terminal && lhs->payload == rhs->payload)
    {
        for (int i = 0; i < num_chars; ++i)
        {
            if (lhs->children[i] != nullptr && rhs->children[i] != nullptr)
            {
                if (!operator_equals_recur(lhs->children[i], rhs->children[i]))
                {
                    return false;
                }
//                is_equal = is_equal && operator_equals_recur(lhs->children[i], rhs->children[i]);
            }
            else if (lhs->children[i] == nullptr && rhs->children[i] == nullptr)
            {
                continue;
            }
            else
            {
                return false;
            }
        }
        return true;
    }
    return false;
}

bool trie::operator==(const trie &rhs) const
{





    return false;
}

bool operator!=(const trie &lhs, const trie &rhs)
{
    return !(lhs == rhs);
}

bool operator<=(const trie &lhs, const trie &rhs)
{
    return false;
}

bool operator>(const trie &lhs, const trie &rhs)
{
    return false;
}

bool operator>=(const trie &lhs, const trie &rhs)
{
    return false;
}



bool trie::operator<(const trie &rhs) const
{
    return false;
}

trie trie::operator&(const trie &rhs) const
{
    return rhs;
}

trie trie::operator|(const trie &rhs) const
{
    return rhs;
}


std::ostream &operator<<(std::ostream &out, const trie &trie)
{
    return out;
}







