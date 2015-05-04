package com.attender.rita.attender;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import com.attender.R;

import java.util.ArrayList;

public class EventAdapter extends ArrayAdapter<String>
{
    private final Context context;
    LayoutInflater lInflater;
    private final ArrayList<Event> events;

    public EventAdapter(Context context, ArrayList<Event> events)
    {
        super(context, R.layout.event);
        this.context = context;
        this.events = events;
        lInflater = (LayoutInflater) context
                .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent)
    {
        View view = convertView;
        if (view == null) {
            view = lInflater.inflate(R.layout.event, parent, false);
        }

        Event ev = getEvent(position);

        ((TextView) view.findViewById(R.id.tvName)).setText(ev.getName());
        ((TextView) view.findViewById(R.id.tvDate)).setText(ev.getDate().toString());

        return view;
    }

    Event getEvent(int position) {
        return events.get(position);
    }

    public long getItemId(int position) {
        return position;
    }

    public int getCount() {
        return events.size();
    }
}