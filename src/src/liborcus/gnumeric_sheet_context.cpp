/*************************************************************************
 *
 * Copyright (c) 2010, 2011 Kohei Yoshida
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

#include "gnumeric_sheet_context.hpp"
#include "gnumeric_cell_context.hpp"
#include "gnumeric_token_constants.hpp"
#include "gnumeric_namespace_types.hpp"
#include "gnumeric_helper.hpp"
#include "orcus/global.hpp"
#include "orcus/spreadsheet/import_interface.hpp"
#include "gnumeric_helper.hpp"

namespace orcus {

namespace {

class gnumeric_style_region_attr_parser : public std::unary_function<xml_token_attr_t, void>
{
public:
    gnumeric_style_region_attr_parser(gnumeric_style_region& style_region_data):
        m_style_region_data(style_region_data) {}

    void operator() (const xml_token_attr_t& attr)
    {
        switch(attr.name)
        {
            case XML_startCol:
            {
                size_t n = atoi(attr.value.get());
                m_style_region_data.start_col = n;
            }
            break;
            case XML_startRow:
            {
                size_t n = atoi(attr.value.get());
                m_style_region_data.start_row = n;
            }
            break;
            case XML_endCol:
            {
                size_t n = atoi(attr.value.get());
                m_style_region_data.end_col = n;
            }
            break;
            case XML_endRow:
            {
                size_t n = atoi(attr.value.get());
                m_style_region_data.end_row = n;
            }
            break;
            default:
                ;
        }
    }

private:
    gnumeric_style_region& m_style_region_data;
};

class gnumeric_font_attr_parser : public std::unary_function<xml_token_attr_t, void>
{
public:
    gnumeric_font_attr_parser(spreadsheet::iface::import_styles& styles) :
        m_styles(styles) {}

    void operator() (const xml_token_attr_t& attr)
    {
        switch(attr.name)
        {
            case XML_Unit:
            {
                double n = atoi(attr.value.get());
                m_styles.set_font_size(n);
            }
            break;
            case XML_Bold:
            {
                bool b = atoi(attr.value.get()) != 0;
                m_styles.set_font_bold(b);
            }
            break;
            case XML_Italic:
            {
                bool b = atoi(attr.value.get()) != 0;
                m_styles.set_font_italic(b);
            }
            break;
            case XML_Underline:
            {
                int n = atoi(attr.value.get());
                switch (n)
                {
                    case 0:
                        m_styles.set_font_underline(spreadsheet::underline_none);
                    break;
                    case 1:
                        m_styles.set_font_underline(spreadsheet::underline_single);
                    break;
                    case 2:
                        m_styles.set_font_underline(spreadsheet::underline_double);
                    break;
                    default:
                        ;
                }
            }
            break;
        }
    }

private:
    spreadsheet::iface::import_styles& m_styles;
};

class gnumeric_style_attr_parser : public std::unary_function<xml_token_attr_t, void>
{
public:
    gnumeric_style_attr_parser(spreadsheet::iface::import_styles& styles) :
        m_styles(styles),
        m_fill(false),
        m_protection(false) {}

    void operator() (const xml_token_attr_t& attr)
    {
        switch(attr.name)
        {
            case XML_Fore:
            {
                spreadsheet::color_elem_t red, green, blue;
                gnumeric_helper::parse_RGB_color_attribute(red, green, blue, attr.value);
                m_styles.set_fill_fg_color(0, red, green, blue);

                m_fill = true;
            }
            break;
            case XML_Back:
            {
                spreadsheet::color_elem_t red, green, blue;
                gnumeric_helper::parse_RGB_color_attribute(red, green, blue, attr.value);
                m_styles.set_fill_bg_color(0, red, green, blue);

                m_fill = true;
            }
            break;
            case XML_Hidden:
            {
                bool b = atoi(attr.value.get());
                m_styles.set_cell_hidden(b);

                m_protection = true;
            }
            break;
            case XML_Locked:
            {
                bool b = atoi(attr.value.get());
                m_styles.set_cell_locked(b);

                m_protection = true;
            }
            break;
            case XML_Format:
            {
                if (attr.value != "General")
                {
                    m_styles.set_number_format(attr.value.get(), attr.value.size());
                    size_t index = m_styles.commit_number_format();
                    m_styles.set_xf_number_format(index);
                }
            }
        }
    }

    bool is_protection_set() const
    {
        return m_protection;
    }

    bool is_fill_set() const
    {
        return m_fill;
    }

private:
    spreadsheet::iface::import_styles& m_styles;

    bool m_fill;
    bool m_protection;
};

}


gnumeric_sheet_context::gnumeric_sheet_context(
    const tokens& tokens, spreadsheet::iface::import_factory* factory) :
    xml_context_base(tokens),
    mp_factory(factory),
    mp_sheet(0)
{
}

gnumeric_sheet_context::~gnumeric_sheet_context()
{
}

bool gnumeric_sheet_context::can_handle_element(xmlns_id_t ns, xml_token_t name) const
{
    if (ns == NS_gnumeric_gnm && name == XML_Cells)
        return false;

    return true;
}

xml_context_base* gnumeric_sheet_context::create_child_context(xmlns_id_t ns, xml_token_t name) const
{
    if (ns == NS_gnumeric_gnm && name == XML_Cells)
        return new gnumeric_cell_context(get_tokens(), mp_factory, mp_sheet);

    return NULL;
}

void gnumeric_sheet_context::end_child_context(xmlns_id_t ns, xml_token_t name, xml_context_base* child)
{
}

void gnumeric_sheet_context::start_element(xmlns_id_t ns, xml_token_t name, const xml_attrs_t& attrs)
{
    push_stack(ns, name);
    if (ns == NS_gnumeric_gnm)
    {
        switch (name)
        {
            case XML_Font:
                start_font(attrs);
            break;
            case XML_Style:
                start_style(attrs);
            break;
            case XML_StyleRegion:
                start_style_region(attrs);
            break;
            default:
                ;
        }
    }
}

bool gnumeric_sheet_context::end_element(xmlns_id_t ns, xml_token_t name)
{
    if (ns == NS_gnumeric_gnm)
    {
        switch(name)
        {
            case XML_Name:
            {
                xml_token_pair_t parent = get_parent_element();
                if(parent.first == NS_gnumeric_gnm && parent.second == XML_Sheet)
                    end_table();
                else
                    warn_unhandled();
            }
            break;
            case XML_Font:
                end_font();
            break;
            case XML_Style:
                end_style();
            break;
            default:
                ;
        }
    }

    return pop_stack(ns, name);
}

void gnumeric_sheet_context::characters(const pstring& str)
{
    chars = str;
}

void gnumeric_sheet_context::start_font(const xml_attrs_t& attrs)
{
    for_each(attrs.begin(), attrs.end(), gnumeric_font_attr_parser(*mp_factory->get_styles()));
}

void gnumeric_sheet_context::start_style(const xml_attrs_t& attrs)
{
    const gnumeric_style_attr_parser& attr_parser = for_each(attrs.begin(), attrs.end(), gnumeric_style_attr_parser(*mp_factory->get_styles()));
    spreadsheet::iface::import_styles& styles = *mp_factory->get_styles();
    if (attr_parser.is_fill_set())
    {
        size_t fill_id = styles.commit_fill();
        styles.set_xf_fill(fill_id);
    }
    if (attr_parser.is_protection_set())
    {
        size_t protection_id = styles.commit_cell_protection();
        styles.set_xf_protection(protection_id);
    }
}

void gnumeric_sheet_context::start_style_region(const xml_attrs_t& attrs)
{
    mp_region_data.reset(new gnumeric_style_region());
    for_each(attrs.begin(), attrs.end(), gnumeric_style_region_attr_parser(*mp_region_data));
}

void gnumeric_sheet_context::end_table()
{
    mp_sheet = mp_factory->append_sheet(chars.get(), chars.size());
}

void gnumeric_sheet_context::end_font()
{
    spreadsheet::iface::import_styles& styles = *mp_factory->get_styles();
    styles.set_font_name(chars.get(), chars.size());
    size_t font_id = styles.commit_font();
    styles.set_xf_font(font_id);
}

void gnumeric_sheet_context::end_style()
{
    spreadsheet::iface::import_styles& styles = *mp_factory->get_styles();
    size_t id = styles.commit_cell_xf();
    mp_region_data->xf_id = id;
}

void gnumeric_sheet_context::end_style_region()
{
    for (spreadsheet::col_t col = mp_region_data->start_col;
            col <= mp_region_data->end_col; ++col)
    {
        for (spreadsheet::row_t row = mp_region_data->start_row;
                row <= mp_region_data->end_row; ++row)
        {
            mp_sheet->set_format(row, col, mp_region_data->xf_id);
        }
    }
    mp_region_data.reset();
}

}
