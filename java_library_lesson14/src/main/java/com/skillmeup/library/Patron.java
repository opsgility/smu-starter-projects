package com.skillmeup.library;

public class Patron {
    private String name;
    private String patronId;
    private String email;

    public Patron(String name, String patronId, String email) {
        this.name = name; this.patronId = patronId; this.email = email;
    }
    public String getName()     { return name; }
    public String getPatronId() { return patronId; }
    public String getEmail()    { return email; }

    @Override
    public String toString() { return "Patron[" + name + ", " + patronId + ", " + email + "]"; }
}
