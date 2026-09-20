package com.skillmeup.vaultly;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import java.security.Key;
import java.util.Date;

@Component
public class JwtUtil {
    @Value("${app.jwt.secret}") private String jwtSecret;
    @Value("${app.jwt.expiration}") private long jwtExpiration;

    private Key getKey() { return Keys.hmacShaKeyFor(jwtSecret.getBytes()); }

    // TODO Exercise 1: Implement generateToken(String username)
    // Use Jwts.builder().setSubject(username).setIssuedAt(new Date()).setExpiration(...)
    //   .signWith(getKey()).compact()
    public String generateToken(String username) {
        return null; // TODO: implement
    }

    // TODO Exercise 2: Implement extractUsername(String token)
    // Use Jwts.parserBuilder().setSigningKey(getKey()).build().parseClaimsJws(token).getBody().getSubject()
    public String extractUsername(String token) {
        return null; // TODO: implement
    }

    // TODO Exercise 3: Implement isTokenValid(String token, String username)
    // Extract username from token, compare with given username, check expiration.
    public boolean isTokenValid(String token, String username) {
        return false; // TODO: implement
    }
}
