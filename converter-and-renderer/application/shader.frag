#version 330

uniform vec4 Color;
uniform bool UseLight;

uniform sampler2D Texture;
uniform bool UseTexture;
uniform bool UseColor;

in vec3 v_vert;
in vec3 v_norm;
in vec3 v_text;

in vec3 v_light;

out vec4 f_color;

void main() {
    float lum = 0.5;
    if (UseLight) {
        lum = dot(normalize(v_norm), normalize(v_vert - v_light));
        lum = acos(lum) / 3.14159265;
        lum = clamp(lum, 0.0, 1.0);
        lum = lum * lum;
        lum = smoothstep(0.0, 1.0, lum);
        lum *= smoothstep(0.0, 80.0, v_vert.z) * 0.3 + 0.7;
        lum = lum * 0.8 + 0.2;
    }
    if (UseTexture) {
        vec3 color = texture(Texture, v_text.xy).rgb;
        if (UseColor) {
            color = color * (1.0 - Color.a) + Color.rgb * Color.a;
        }
        f_color = vec4(color * lum, 1.0);
    } else {
        f_color = vec4(Color.rgb * lum, Color.a);
    }
}
