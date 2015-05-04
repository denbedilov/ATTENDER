package com.attender.rita.attender;
import java.sql.Time;
import java.util.Date;

/**
 *
 */
public class Event
{
    public Event(String id, String date, String name, String time, String address, String description, String performer)
    {
        setId(id);
        setDate(date);
        setName(name);
        setTime(time);
        setAddress(address);
        setDescription(description);
        setPerformer(performer);
    }
    private int _id;
    private String _date;
    private String _name;
    private String _time;
    private String _address;
    private String _description;
    private String _performer;

    public int getId() {
        return _id;
    }

    public void setId(String id) {
        _id = Integer.parseInt(id);
    }

    public String getDate() {
        return _date;
    }

    public void setDate(String date) {
        _date = date;
    }

    public String getName() {
        return _name;
    }

    public void setName(String name) {
        _name = name;
    }

    public String getTime() {
        return _time;
    }

    public void setTime(String time) {
        _time = time;
    }

    public String getAddress() {
        return _address;
    }

    public void setAddress(String address) {
        _address = address;
    }

    public String getDescription() {
        return _description;
    }

    public void setDescription(String description) {
        _description = description;
    }

    public String getPerformer() {
        return _performer;
    }

    public void setPerformer(String performer) {
        _performer = performer;
    }
}
// add constructor for pull from DB
// add setters and getters
