#version 120

uniform vec3 near11;
uniform vec3 near12;
uniform vec3 near21;
uniform vec3 near22;
uniform vec3 far11;
uniform vec3 far12;
uniform vec3 far21;
uniform vec3 far22;

uniform vec2 res;

void CalcRay(inout vec3 rayOrigin, inout vec3 rayDirection) {
	float x= gl_FragCoord.x/res.x , y= gl_FragCoord.y/res.y , z;
	vec3 l,r;
	l= near11+y*(near12-near11);
	r= near21+y*(near22-near21);
	vec3 p1= l+x*(r-l);
	l= far11+y*(far12-far11);
	r= far21+y*(far22-far21);
	vec3 p2= l+x*(r-l);
	rayOrigin= p2; // because unprojector is wonky
	rayDirection= normalize(p2-p1);
	rayOrigin-=rayDirection;
}


uniform vec3 c1;
uniform vec3 c2;
float cRadius=1.0;

// InterectRaySphere rayEye rayDir sphereCentre sphereRadius &tval &pnt =
bool RaySphereIntersect(vec3 o, vec3 d, vec3 p, float r, inout vec3 I) {
	vec3 m = o - p;
	float b = dot(m,d);
	float c = dot(m,m) - r * r;
	if (c > 0.0 && b > 0.0) return false;
	float discr = b * b - c;
	if (discr < 0.0) return false;
	float tval = -b - sqrt(discr);
	if (tval < 0.0) tval = 0.0;
	I = o + tval	* d;
	return true;
}


bool RayPlaneIntersect( vec3 p, vec3 d, vec3 pUp, inout vec3 I ) {
	float     D = dot(pUp, d);
	float     N = -dot(pUp, p);
	
	if (abs(D) < 1e-08)	// segment is parallel to plane
		return false;

	// they are not parallel
	// compute intersect param
	float sI = N / D;
	if (sI<0)
		return false;                        // plane is behind ray

    I = p + sI * d;
    return true;
}
	
float pointLineDist( vec3 P, vec3 lo, vec3 ld) {
	vec3 w = P - lo;
	
	float c1 = dot(w,ld);
	float c2 = dot(ld,ld);
	float b = c1 / c2;
	
	vec3 Pb = lo + b * ld;
	return length(P-Pb);
}

float pointRayDist( vec3 P, vec3 lo, vec3 ld) {
	vec3 w = P - lo;
	
	float c1 = dot(w,ld);
	float c2 = dot(ld,ld);
	float b = c1 / c2;
	float l = length(P-(lo + b * ld));
	return b>0 ? l : length(P-lo) ; // ? idk. w/e
}

float taxi(vec3 p1,vec3 p2) {vec3 d=p1-p2;return abs(d.x)+abs(d.y)+abs(d.z);}
float taxi(vec2 p1,vec2 p2) {vec2 d=p1-p2;return abs(d.x)+abs(d.y);}
float taxi(vec2 p1) {return taxi(p1,vec2(0));}
float taxi(vec3 p1) {return taxi(p1,vec3(0));}

float cheby(vec3 p1,vec3 p2) {vec3 d=p1-p2;return max(max(abs(d.x),abs(d.y)),abs(d.z));}
float cheby(vec2 p1,vec2 p2) {vec2 d=p1-p2;return max(abs(d.x),abs(d.y));}
float cheby(vec2 p1) {return cheby(p1,vec2(0));}
float cheby(vec3 p1) {return cheby(p1,vec3(0));}

float grid_fade_otherSides(vec3 o, vec3 p) {
	vec3 d= p*o;
	float f=1.0;
	if (d.x<0) f/=4.0;
	if (d.y<0) f/=4.0;
	if (d.z<0) f/=4.0;
	return f;
}

vec3 H=vec3(.5);
void grid(vec3 o, vec3 d, vec3 P) {
	vec3 I;
	if (RayPlaneIntersect( o,d, P,  I )) {
		vec3 i= I*(vec3(1)-P);
		float f= length(fract(i)-H);
		f/= max( cheby(I)-4 ,1);
		f*= grid_fade_otherSides(o,I);
		//f= smoothstep(.0,.125, f );
		gl_FragColor.g+= f/4;
	}
}

void green_grid(vec3 o, vec3 d) {
	grid(o,d,vec3(1,0,0));
	grid(o,d,vec3(0,1,0));
	grid(o,d,vec3(0,0,1));
}

int region(vec3 p) {
	float d1=taxi(p,c1);
	float d2=taxi(p,c2);
	if (d1<d2) return 1;
	if (d2<d1) return 2;
	return 0;
}

//	for point p which lies virtually equidistant between spheres (in taxi metric),
// sample points around it using 3x3x3 spread.
// usage, python equiv: a=[v for v in spread if Region(p+v)==Region(camPos)];norm=sum(a)/len(a)
#define spread_sz 26
vec3 spread[spread_sz] = vec3[](
	vec3(-1.0,-1.0,-1.0),
	vec3( 0.0,-1.0,-1.0),
	vec3( 1.0,-1.0,-1.0),
	vec3(-1.0, 0.0,-1.0),
	vec3( 0.0, 0.0,-1.0),
	vec3( 1.0, 0.0,-1.0),
	vec3(-1.0, 1.0,-1.0),
	vec3( 0.0, 1.0,-1.0),
	vec3( 1.0, 1.0,-1.0),
	vec3(-1.0,-1.0, 0.0),
	vec3( 0.0,-1.0, 0.0),
	vec3( 1.0,-1.0, 0.0),
	vec3(-1.0, 0.0, 0.0),
	vec3( 1.0, 0.0, 0.0),
	vec3(-1.0, 1.0, 0.0),
	vec3( 0.0, 1.0, 0.0),
	vec3( 1.0, 1.0, 0.0),
	vec3(-1.0,-1.0, 1.0),
	vec3( 0.0,-1.0, 1.0),
	vec3( 1.0,-1.0, 1.0),
	vec3(-1.0, 0.0, 1.0),
	vec3( 0.0, 0.0, 1.0),
	vec3( 1.0, 0.0, 1.0),
	vec3(-1.0, 1.0, 1.0),
	vec3( 0.0, 1.0, 1.0),
	vec3( 1.0, 1.0, 1.0));

#define EPS 1e-04
vec3 TaxiNorm(vec3 p) {
	int nc=0,r=region(p);
	vec3 norm=vec3(0.0,0.0,0.0);
	for (int i=0;i<spread_sz;i++) {
		if (region(p+spread[i]*EPS) != r) {
			norm+= spread[i];
			nc+=1;
		}
	}
	return norm/nc;
}
	


void _taxi_plane(vec3 rOrig, vec3 rDir) {
	vec3 p=rOrig,cp= (c1+c2)/2.0;
	float maxDist= max(length(rOrig-c1),length(rOrig-c2))*2.0;
	float sphDist= length(c1-c2);
	float l, lMin=0.0,lMax= length(rOrig-cp)*2.0; // hence the far clip
	int r, r1=region(rOrig+rDir*lMin), r2=region(rOrig+rDir*lMax);

	if (r1!=r2) {
		while (lMax-lMin>1e-05) {
			l= (lMin+lMax)/2.0;
			p= rOrig+rDir*l;
			r= region(p);
			if (r==r1) lMin=l;
			if (r!=r1) lMax=l;
		}
		
		vec3 n= TaxiNorm(p);
		if (r!=r1) n*=-1.0;
		gl_FragColor= vec4(vec3(dot(rDir,n)),1.0);
	}
}
	
// todo: try ray-taxiSphere intersect
void taxi_plane(vec3 o, vec3 d) {
	vec3 cp= (c1+c2)/2;
	float cs= length(c1-c2);
	vec3 I;
	if (RaySphereIntersect(o,d,cp,cs,I)) _taxi_plane(o,d);
}
					
void main() {
	vec3 p,d;CalcRay(p,d);

	float d1=pointRayDist( c1, p,d);
	float d2=pointRayDist( c2, p,d);

	gl_FragColor= vec4(vec3(0),.5);
	green_grid(p,d);
	taxi_plane(p,d);

	vec3 I;
	if (RaySphereIntersect(p,d,c1,1.,I)) {gl_FragColor.r=(length(I-c1));}
	if (RaySphereIntersect(p,d,c2,1.,I)) {gl_FragColor.b=(length(I-c2));}
	
	//gl_FragColor = vec4(vec3(gl_FragCoord.z),1);
}



