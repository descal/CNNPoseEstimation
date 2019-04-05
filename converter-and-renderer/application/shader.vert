#version 330

uniform mat4 M;
uniform mat4 V;
uniform mat4 P;
uniform vec3 Light;

in vec3 in_vert;
in vec3 in_norm;
in vec3 in_text;

out vec3 v_vert;
out vec3 v_norm;
out vec3 v_text;

out vec3 v_light;

void main() {
    v_vert = in_vert;
    v_norm = in_norm;
    v_text = in_text;
    v_light = (P * M * vec4(Light, 1.0)).xyz;
    gl_Position = P * V * M * vec4(v_vert, 1.0);
}

