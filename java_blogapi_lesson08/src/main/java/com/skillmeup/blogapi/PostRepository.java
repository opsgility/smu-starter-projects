package com.skillmeup.blogapi;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;
public interface PostRepository extends JpaRepository<Post, Long> {
    @Query("SELECT p FROM Post p WHERE p.author.id = :authorId ORDER BY p.createdAt DESC")
    List<Post> findByAuthorId(@Param("authorId") Long authorId);
    @Query("SELECT p FROM Post p WHERE p.title LIKE %:keyword% OR p.content LIKE %:keyword%")
    List<Post> searchByKeyword(@Param("keyword") String keyword);
    @Query(value="SELECT p.* FROM posts p LEFT JOIN comments c ON p.id=c.post_id GROUP BY p.id ORDER BY COUNT(c.id) DESC LIMIT :limit", nativeQuery=true)
    List<Post> findTopCommented(@Param("limit") int limit);
}
