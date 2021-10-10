#pragma once

#include <Grid.hpp>
#include <glm/glm.hpp>
#include <memory>
#include <unordered_set>

namespace griddly {

struct SearchOutput {
  glm::ivec2 direction;
};

class PathFinder {
 public:
  PathFinder(std::shared_ptr<Grid> grid, std::unordered_set<std::string> passableObjects, std::unordered_set<std::string> impassableObjects);

  virtual SearchOutput search(glm::ivec2 startLocation, glm::ivec2 endLocation, uint32_t maxDepth) = 0;

 protected:
  const std::shared_ptr<Grid> grid_;
  std::unordered_set<std::string> passableObjects_;
  std::unordered_set<std::string> impassableObjects_;
};

}  // namespace griddly