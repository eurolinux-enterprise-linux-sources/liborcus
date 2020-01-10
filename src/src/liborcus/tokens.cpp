/*************************************************************************
 *
 * Copyright (c) 2010 Kohei Yoshida
 * 
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 * 
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 *
 ************************************************************************/

#include "orcus/tokens.hpp"
#include "orcus/pstring.hpp"

using namespace std;

namespace orcus {

tokens::tokens(const char** token_names, size_t token_name_count) :
    m_token_names(token_names), 
    m_token_name_count(token_name_count)
{
    for (size_t i = 0; i < m_token_name_count; ++i)
    {
        m_tokens.insert(
            token_map_type::value_type(
                pstring(m_token_names[i]), static_cast<xml_token_t>(i)));
    }
}

bool tokens::is_valid_token(xml_token_t token) const
{
    return token != XML_UNKNOWN_TOKEN;
}

xml_token_t tokens::get_token(const pstring& name) const
{
    token_map_type::const_iterator itr = m_tokens.find(name);
    if (itr == m_tokens.end())
        return XML_UNKNOWN_TOKEN;
    return itr->second;
}

const char* tokens::get_token_name(xml_token_t token) const
{
    if (static_cast<size_t>(token) >= m_token_name_count)
        return "";

    return m_token_names[token];
}

}
