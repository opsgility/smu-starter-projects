package com.skillmeup.vaultly;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import java.io.IOException;

// TODO Exercise 4: Implement JWT authentication filter.
// Inject JwtUtil and CustomUserDetailsService via constructor.
// In doFilterInternal:
//   1. Read Authorization header — if null or doesn't start with "Bearer ", call filterChain.doFilter() and return
//   2. Extract the token (substring after "Bearer ")
//   3. Extract username from token using jwtUtil.extractUsername(token)
//   4. If username is non-null and SecurityContextHolder has no authentication:
//      - Load UserDetails via userDetailsService.loadUserByUsername(username)
//      - If jwtUtil.isTokenValid(token, username) is true:
//          - Create UsernamePasswordAuthenticationToken with userDetails and authorities
//          - Set details using WebAuthenticationDetailsSource
//          - Set in SecurityContextHolder.getContext().setAuthentication(...)
//   5. Always call filterChain.doFilter(request, response) at the end
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtUtil jwtUtil;
    private final CustomUserDetailsService userDetailsService;

    public JwtAuthenticationFilter(JwtUtil jwtUtil,
                                   CustomUserDetailsService userDetailsService) {
        this.jwtUtil = jwtUtil;
        this.userDetailsService = userDetailsService;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {
        // TODO: implement JWT extraction and validation
        filterChain.doFilter(request, response);
    }
}
