/*************************************************************************
 *
 * Copyright (c) 2013 Kohei Yoshida
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

#ifndef __ORCUS_ZIP_ARCHIVE_HPP__
#define __ORCUS_ZIP_ARCHIVE_HPP__

#include "env.hpp"
#include <cstdlib>
#include <exception>
#include <string>
#include <vector>

#include <boost/unordered_map.hpp>

namespace orcus {

class zip_archive_stream;
class zip_archive_impl;
class pstring;

class ORCUS_DLLPUBLIC zip_error : public std::exception
{
    std::string m_msg;
public:
    zip_error();
    zip_error(const std::string& msg);
    virtual ~zip_error() throw();

    virtual const char* what() const throw();
};

class ORCUS_DLLPUBLIC zip_archive
{
    zip_archive_impl* mp_impl;

    zip_archive(); // disabled
    zip_archive(const zip_archive&); // disabled
    zip_archive& operator= (const zip_archive); // disabled

public:
    zip_archive(zip_archive_stream* stream);
    ~zip_archive();

    /**
     * Loading involves the parsing of the central directory of a zip archive
     * (located toward the end of the stream) and building of file entry data
     * which are stored in the central directory.
     */
    void load();

    /**
     * Dump the content of a specified file entry to stdout.
     *
     * @param index file entry index
     */
    void dump_file_entry(size_t index) const;

    /**
     * Dump the content of a specified file entry to stdout.
     *
     *
     * @param entry_name file entry name.
     */
    void dump_file_entry(const char* entry_name) const;

    /**
     * Get file entry name from its index.
     *
     * @param index file entry index
     *
     * @return file entry name
     */
    pstring get_file_entry_name(size_t index) const;

    /**
     * Return the number of file entries stored in this zip archive.  Note
     * that a file entry may be a directory, so the number of files stored in
     * the zip archive may not equal the number of file entries.
     *
     * @return number of file entries.
     */
    size_t get_file_entry_count() const;

    /**
     * Retrieve data stream of specified file entry into buffer. The retrieved
     * data stream gets uncompressed if the original stream is compressed.
     * The method will overwrite the content of passed buffer if there is any
     * pre-existing data in it.
     *
     * @param entry_name file entry name
     * @param buf buffer to put the retrieved data stream into.
     *
     * @return true if successful, false otherwise.
     */
    bool read_file_entry(const pstring& entry_name, std::vector<unsigned char>& buf) const;
};

}

#endif
