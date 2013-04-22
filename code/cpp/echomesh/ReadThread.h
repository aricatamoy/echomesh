#ifndef __ECHOMESH_READ_THREAD__
#define __ECHOMESH_READ_THREAD__

#include <stdio.h>

#include <istream>
#include <vector>

#include "yaml-cpp/yaml.h"
#include "echomesh/LightConfig.h"

namespace echomesh {

class LineGetter;

class ReadThread : public Thread {
 public:
  ReadThread(const String& commandLine);
  virtual ~ReadThread();
  virtual void run();
  void handleMessage(const string&);
  virtual void quit() = 0;
  void kill();

 protected:
  virtual void parseNode() = 0;

  YAML::Node node_;
  string type_;
  StringArray accum_;
  ScopedPointer<LineGetter> lineGetter_;

  DISALLOW_COPY_AND_ASSIGN(ReadThread);
};

}  // namespace echomesh

#endif // __ECHOMESH_READ_THREAD__
