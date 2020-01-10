/*************************************************************************
 *
 * Copyright (c) 2012 Kohei Yoshida
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

#ifndef __ORCUS_SPREADSHEET_EXPORT_INTERFACE_HPP__
#define __ORCUS_SPREADSHEET_EXPORT_INTERFACE_HPP__

#include "types.hpp"
#include "../env.hpp"

#include <ostream>

namespace orcus { namespace spreadsheet { namespace iface {

class export_sheet
{
public:
    ORCUS_DLLPUBLIC virtual ~export_sheet() = 0;

    virtual void write_string(std::ostream& os, orcus::spreadsheet::row_t row, orcus::spreadsheet::col_t col) const = 0;
};

class export_factory
{
public:
    ORCUS_DLLPUBLIC virtual ~export_factory() = 0;

    virtual const export_sheet* get_sheet(const char* sheet_name, size_t sheet_name_length) const = 0;
};

}}}




#endif
