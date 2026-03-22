"""Macros for generating proto libraries."""

load("@protobuf//bazel:proto_library.bzl", "proto_library")
load("@protobuf//bazel:py_proto_library.bzl", "py_proto_library")
load("@protobuf//bazel:java_proto_library.bzl", "java_proto_library")
load("@rules_go//proto:def.bzl", "go_proto_library")
load("@rules_swift//proto:proto.bzl", "swift_proto_library")

def proto_libraries(
    name,
    srcs,
    go_base,
    deps = []):
  """Generates proto libraries for go, python, java & swift.

  Args:
    name: The name of the proto library.
    srcs: The list of .proto files to include in the library.
    go_base: The base import path for the generated Go code.
    deps: A list of dependencies for the proto library.
  """
  proto_library_name = name + "_proto"
  proto_library_dep = ":" + proto_library_name

  proto_library(
    name = proto_library_name,
    srcs = srcs,
    deps = deps,
    visibility = ["//visibility:public"],
  )

  go_proto_library(
    name = name + "_go_proto",
    importpath = go_base + "/" + name,
    proto = proto_library_dep,
    visibility = ["//visibility:public"],
    deps = [
      "//third_party/protovalidate:validate_go_proto",
    ],
  )

  py_proto_library(
    name = name + "_py_proto",
    deps = [proto_library_dep],
    visibility = ["//visibility:public"],
  )

  java_proto_library(
    name = name + "_java_proto",
    deps = [proto_library_dep],
    visibility = ["//visibility:public"],
  )

  swift_proto_library(
    name = name + "_swift_proto",
    protos = [proto_library_dep],
    visibility = ["//visibility:public"],
  )
