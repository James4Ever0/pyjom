/*
 * Copyright (C) 2018-2019 Werner Turing <werner.turing@protonmail.com>
 *
 * This file is part of multi-delogo.
 *
 * multi-delogo is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * multi-delogo is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with multi-delogo.  If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef FG_EXCEPTIONS_H
#define FG_EXCEPTIONS_H

#include <exception>

namespace fg {
  class Exception : public std::exception
  {
    virtual const char* what() const throw() = 0;
  };


  class InvalidFilterException : public Exception
  {
  public:
    virtual const char* what() const throw()
    {
        return "Invalid filter line";
    }
  };


  class UnknownFilterException : public Exception
  {
  public:
    virtual const char* what() const throw()
    {
        return "Unknown filter";
    }
  };


  class InvalidParametersException : public Exception
  {
  public:
    virtual const char* what() const throw()
    {
        return "Invalid parameters for filter";
    }
  };


  class InvalidFilterDataException : public Exception
  {
  public:
    virtual const char* what() const throw()
    {
        return "Invalid filter data file";
    }
  };
}


#endif // FG_EXCEPTIONS_H
